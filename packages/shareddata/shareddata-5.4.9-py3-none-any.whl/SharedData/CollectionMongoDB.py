import pandas as pd
import numpy as np
import datetime
import math

from SharedData.Database import *
from SharedData.Utils import datetype
from pymongo import ASCENDING,UpdateOne
from SharedData.Logger import Logger

class CollectionMongoDB:

    # TODO: create partitioning option yearly, monthly, daily
    def __init__(self, shareddata, database, period, source, tablename,
                 records=None, names=None, formats=None, size=None, hasindex=True,
                 overwrite=False, user='master', tabletype=1, partitioning=None):
        # tabletype 1: DISK, 2: MEMORY
        self.type = tabletype

        self.shareddata = shareddata
        self.user = user
        self.database = database
        self.period = period
        self.source = source
        self.tablename = tablename
        self.subscription_thread = None
        self.publish_thread = None

        self.names = names
        self.formats = formats
        self.size = size
        if not size is None:
            if size == 0:
                self.hasindex = False
        self.hasindex = hasindex
        self.overwrite = overwrite
        self.partitioning = partitioning
                
        self._collection = None

        self.mongodb = self.shareddata.mongodb
        self.mongodb_client = self.mongodb.client[self.user]
        
        self.path = f'{user}/{database}/{period}/{source}/collection/{tablename}'
        self.relpath = f'{database}/{period}/{source}/collection/{tablename}'
        self.pkey_columns = DATABASE_PKEYS[self.database]
        if self.relpath not in self.mongodb_client.list_collection_names():
            # Create collection            
            self.mongodb_client.create_collection(self.relpath)                        
            index_fields = [(f"{field}", ASCENDING) for field in self.pkey_columns]
            self.mongodb_client[self.relpath].create_index(index_fields, unique=True)

        self._collection = self.mongodb_client[self.relpath]

    @property
    def collection(self):
        return self._collection

    def upsert(self, data):
        """
        Perform upsert operations on the collection. Can handle a single document or multiple documents.

        :param data: A dictionary representing a single document to be upserted,
                     or a list of such dictionaries for multiple documents.
        """
        # If data is a dictionary, convert it into a list so both cases are handled uniformly
        if isinstance(data, dict):
            data = [data]
        
        operations = []
        missing_pkey_items = []
        for item in data:
            # Check if the item contains all primary key columns
            if not all(field in item for field in self.pkey_columns):
                missing_pkey_items.append(item)
                continue  # Skip this item if it doesn't contain all primary key columns

            # Check if date needs to be floored to specific intervals
            if 'date' in item:
                if self.period == 'D1':
                    item = item.copy()
                    item['date'] = pd.Timestamp(item['date']).normalize()
                elif self.period == 'M15':
                    item = item.copy()
                    item['date'] = pd.Timestamp(item['date']).floor('15T')                
                elif self.period == 'M1':
                    item = item.copy()
                    item['date'] = pd.Timestamp(item['date']).floor('T')
                
            # Construct the filter condition using the primary key columns
            filter_condition = {field: item[field] for field in self.pkey_columns if field in item}
            
            # Prepare the update operation
            update_data = {'$set': item}

            # Add the upsert operation to the operations list
            operations.append(UpdateOne(filter_condition, update_data, upsert=True))
        
        # Execute all operations in bulk if more than one, otherwise perform single update
        if len(operations) > 0:
            result = self._collection.bulk_write(operations)

        if len(missing_pkey_items) > 0:
            Logger.log.error(f"{len(missing_pkey_items)}/{len(data)} items were skipped because they didn't contain all primary key columns.")
        
        return result
    
    def find(self, query, projection=None, sort=None, limit=None, skip=None):
        """
        Find documents in the collection based on the provided query.
        Args:
            query (dict): The query to filter documents.
            projection (dict): The fields to include or exclude in the result.
            sort (list): The fields to sort the result by.
            limit (int): The maximum number of documents to return.
            skip (int): The number of documents to skip before returning results.
        Returns:
            list: A list of documents that match the query.
        """
        if projection:
            cursor = self._collection.find(query, projection)
        else:
            cursor = self._collection.find(query)
        if sort:
            cursor = cursor.sort(sort)
        if skip:
            cursor = cursor.skip(skip)
        if limit:
            cursor = cursor.limit(limit)
        return list(cursor)
    
    def delete(self, query):
        """
        Delete documents from the collection based on the provided query.
        Args:
            query (dict): The query to filter documents to be deleted.
        Returns:
            int: The number of documents deleted.
        """
        result = self._collection.delete_many(query)
        return result.deleted_count
    
    @staticmethod
    def serialize(obj):
        """
        Recursively serialize any Python object into a nested dict/list structure,
        removing "empty" values as defined by is_empty().
        """

        # 1) Special-case Timestamps so they don't get recursed:
        if isinstance(obj, pd.Timestamp):
            # Return None if it's considered 'empty' (e.g. NaT),
            # otherwise treat it as a scalar (string, raw Timestamps, etc.)
            return None if CollectionMongoDB.is_empty(obj) else obj

        # 2) Dict
        if isinstance(obj, dict):
            new_dict = {}
            for k, v in obj.items():
                # Recurse
                serialized_v = CollectionMongoDB.serialize(v)
                # Only keep non-empty values
                if serialized_v is not None and not CollectionMongoDB.is_empty(serialized_v):
                    new_dict[k] = serialized_v

            # If the resulting dict is empty, return None instead of {}
            return new_dict if new_dict else None

        # 3) DataFrame
        if isinstance(obj, pd.DataFrame):
            records = obj.to_dict(orient='records')
            # Each record is a dict, so we re-serialize it
            return [
                r for r in (CollectionMongoDB.serialize(rec) for rec in records)
                if r is not None and not CollectionMongoDB.is_empty(r)
            ]

        # 4) List/tuple/set
        if isinstance(obj, (list, tuple, set)):
            new_list = [
                CollectionMongoDB.serialize(item)
                for item in obj
                if not CollectionMongoDB.is_empty(item)
            ]
            # If the list ends up empty, return None
            return new_list if new_list else None

        # 5) For other objects with __dict__, treat them like a dict
        if hasattr(obj, "__dict__"):
            return CollectionMongoDB.serialize(vars(obj))

        # 6) Otherwise, just return the raw value if it's not "empty"
        return obj if not CollectionMongoDB.is_empty(obj) else None

    EMPTY_VALUES = {
        str: ["", "1.7976931348623157E308", "0.0", "nan", "NaN",],
        int: [0, 2147483647],
        float: [0.0, 1.7976931348623157e+308, np.nan, np.inf, -np.inf],
        datetime.datetime: [datetime.datetime(1, 1, 1, 0, 0)],
        pd.Timestamp: [pd.Timestamp("1970-01-01 00:00:00")],
        pd.NaT: [pd.NaT],
        pd.Timedelta: [pd.Timedelta(0)],
        pd.Interval: [pd.Interval(0, 0)],
        type(None): [None],
        bool: [False],
    }

    @staticmethod
    def is_empty(value):
        """
        Returns True if 'value' is a known sentinel or should be treated as empty.
        """
        # Special handling for floats
        if isinstance(value, float):
            if math.isnan(value) or math.isinf(value):
                return True
            if value in (0.0, 1.7976931348623157e+308):
                return True

        # If it's a Timestamp and is NaT, treat as empty
        if isinstance(value, pd.Timestamp):
            if pd.isna(value):  # True for pd.NaT
                return True

        # Check if value is in our known empty sets
        value_type = type(value)
        if value_type in CollectionMongoDB.EMPTY_VALUES:
            if value in CollectionMongoDB.EMPTY_VALUES[value_type]:
                return True

        # Empty containers
        if isinstance(value, (list, tuple, set)) and len(value) == 0:
            return True
        if isinstance(value, dict) and len(value) == 0:
            return True

        return False

