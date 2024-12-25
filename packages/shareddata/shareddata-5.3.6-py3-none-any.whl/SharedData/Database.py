DATABASE_PKEYS = {
    'Symbols':          ['symbol'],
    'Portfolios':       ['portfolio'],
    'Tags':             ['tag'],
    
    'TimeSeries':       ['date'],    
    'MarketData':       ['date', 'symbol'],
    'Relationships':    ['date', 'symbol', 'symbol1'],
    'MarketDataOptions':['date', 'symbol', 'expiry', 'strike', 'callput'],
    
    'Tags':             ['date', 'tag', 'symbol'],
    
    'Portfolios':       ['date', 'portfolio'],        
    'Signals':          ['date', 'portfolio', 'symbol'],
    'Risk':             ['date', 'portfolio', 'symbol'],
    'Positions':        ['date', 'portfolio', 'symbol'],
    'Requests':         ['date', 'portfolio', 'symbol', 'requestid'],
    'Orders':           ['date', 'portfolio', 'symbol', 'clordid'],
    'Trades':           ['date', 'portfolio', 'symbol', 'tradeid']
}

STRING_FIELDS = ['symbol','tag','portfolio','requestid','clordid','tradeid']