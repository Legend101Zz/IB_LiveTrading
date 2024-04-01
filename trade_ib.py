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
        global position

        df=pd.DataFrame(bars)[['date','open','high','low','close']]
        df['SMA'] = calculate_sma(df, sma_length)
        df.set_index('date',inplace=True)
        clear_output(wait=True)
        display(df)
        ma1 = df['SMA'][-2]  
        ma2 = df['SMA'][-1]  
        close = df['close'][-1]  
        high = df['high'][-2]  
        low = df['low'][-2] 

        if ma2 > ma1 and not position:  
            if close < ma2:
                order = MarketOrder('BUY', 1)
                trade = ib.placeOrder(contract, order)
                position = 'long'
                print("Buy order placed.")

        elif ma2 < ma1 and not position:  
            if close > ma2:
                order = MarketOrder('SELL', 1)
                trade = ib.placeOrder(contract, order)
                position = 'short'
                print("Sell order placed.")

        elif position == 'long':  
            if close > ma2 and close < low:
                ib.placeOrder(contract, MarketOrder('SELL', 1))
                position = ''
                print("Take profit order placed for long position.")

        elif position == 'short': 
            if close < ma2 and close > high:
                ib.placeOrder(contract, MarketOrder('BUY', 1))
                position = ''
                print("Take profit order placed for short position.")


    position = ''
    bars.updateEvent += onBarUpdate

    ib.run()