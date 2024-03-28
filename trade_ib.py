import pandas as pd
from lightweight_charts import Chart
import pandas_ta as ta
from ib_insync import *
from IPython.display import display, clear_output

if __name__ == '__main__':
    ib = IB()
    ib.connect('127.0.0.1', 7497, clientId=13)
 
    contract= Crypto('BTC','PAXOS','USD')

    bars=ib.reqHistoricalData(
        contract,
        endDateTime='',
        durationStr='60 S',
        barSizeSetting='5 secs',
        whatToShow='MIDPOINT',
        useRTH=True,
        formatDate=2,
        keepUpToDate=True)
                
    df = util.df(bars)
    sma_length = 5
    df['SMA'] = df['close'].rolling(window=sma_length).mean()
    display(df)
    # chart = Chart()
    # chart.set(df)
    # chart.show()

    def calculate_sma(data, length):
        return data['close'].rolling(window=length).mean()

    def orderFilled(trade, fill):
        print("order has been filled")
        print(trade)
        print(fill)
        print(dir(fill))
        # chart.marker(text=f"order filled at {fill.execution.avgPrice}")
        print(f"order filled at {fill.execution.avgPrice}")



    def onBarUpdate(bars, hasNewBar):

        df=pd.DataFrame(bars)[['date','open','high','low','close']]
        df['SMA'] = calculate_sma(df, sma_length)
        df.set_index('date',inplace=True)
        clear_output(wait=True)
        display(df)
        # last_bar = bars[-1]

        # last_bar_series = pd.Series({
        #     'time': last_bar.time,
        #     'open': last_bar.open_,
        #     'high': last_bar.high,
        #     'low': last_bar.low,
        #     'close': last_bar.close,
        #     'volume': last_bar.volume
        # })

        # print(last_bar_series)

        # chart.update(last_bar_series)
        # order = MarketOrder('BUY', 1)
        # trade = ib.placeOrder(contract, order)
        # trade.fillEvent += orderFilled
        # if len(bars) >= 3:
        #     if bars[-1].close > bars[-1].open_ and \
        #         bars[-2].close > bars[-2].open_ and \
        #         bars[-3].close > bars[-3].open_:
                
        #         print("3 green bars, let's buy!")

        #         # buy 10 shares and call orderFilled() when it fills
        #         order = MarketOrder('BUY', 1)
        #         trade = ib.placeOrder(contract, order)
        #         trade.fillEvent += orderFilled

    bars.updateEvent += onBarUpdate

    ib.run()