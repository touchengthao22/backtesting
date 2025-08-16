import yfinance as yf
import pandas as pd
import pytz

class Backtesting:
    def __init__(self, profit_target: float, stop_loss: float):
        self.profit_target = profit_target
        self.stop_loss = stop_loss
        self.data = None
    
    def get_data(self, ticker: str):
        spy_data = yf.download(ticker, period="5d", interval="5m")

        df = pd.DataFrame(spy_data)
        df.columns = ['_'.join(col).lower() for col in df.columns]
        df.index = df.index.tz_convert('US/Pacific')
        # df.index = df.index.strftime('%Y-%m-%d %I:%M %p')

        cols_to_round = ['close_spy', 'open_spy', 'high_spy', 'low_spy']
        df[cols_to_round] = df[cols_to_round].round(2)


        self.data = df
    
    def show_data(self):
        return self.data.head()
    
    def backtest_orb(self):
        count = 0
       
        for date, group in self.data.groupby(self.data.index.date):
            print("")
            orb_high = group["high_spy"].iloc[0]
            orb_low = group["low_spy"].iloc[0]
            print("-" * 50)
            print(f'orb_high: {orb_high} and orb_low: {orb_low}')
            print("-" * 50)
            
            for i in range(len(group)):
                open_spy = group["open_spy"].iloc[i]
                high = group["high_spy"].iloc[i]
                low = group["low_spy"].iloc[i]
                close = group["close_spy"].iloc[i]

                if open_spy > orb_high and low <= orb_high and close >= orb_high:
                    count += 1
                    print(f"{group.index[i]}, low: {low}, close: {close}")



        print(count)

if __name__ == "__main__":
    bt = Backtesting(10,5)
    bt.get_data("SPY")
    # print(bt.show_data())
    # print(bt.data.dtypes)
    bt.backtest_orb()