import pandas as pd
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
        
        for item in data:
            # Check if the item contains all primary key columns
            if not all(field in item for field in self.pkey_columns):
                Logger.log.error(f"upsert missing pkey: {item}")
                continue  # Skip this item if it doesn't contain all primary key columns

            # Check if date needs to be floored to specific intervals
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
        if len(operations) > 1:
            result = self._collection.bulk_write(operations)
        else:
            result = self._collection.bulk_write([operations[0]])
        
        return result