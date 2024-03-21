from ib_insync import *
# util.startLoop()  # uncomment this line when in a notebook

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)

## ========= TO GET HISTORICAL DATA ========= ##

contract = Forex('EURUSD')
bars = ib.reqHistoricalData(
    contract, endDateTime='', durationStr='30 D',
    barSizeSetting='1 hour', whatToShow='MIDPOINT', useRTH=True)

# convert to pandas dataframe (pandas needs to be installed):
df = util.df(bars)
# print(df) 

market_data =ib.reqMktData(contract,'',False,False ) 


print(market_data)


def onPendingTickers(tickers):
    print("Pending ticker event received")
    print(tickers)

ib.pendingTickersEvent += onPendingTickers

ib.run()