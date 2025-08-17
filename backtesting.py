import yfinance as yf
import pandas as pd
import pytz

class Backtesting:
    def __init__(self, profit_target: float, stop_loss: float):
        self.profit_target = profit_target
        self.stop_loss = stop_loss
        self.data = None
    
    def get_data(self, ticker: str):
        spy_data = yf.download(ticker, period="10d", interval="5m")

        df = pd.DataFrame(spy_data)
        df.columns = ['_'.join(col).lower() for col in df.columns]
        df.index = df.index.tz_convert('US/Pacific')
        # df.index = df.index.strftime('%Y-%m-%d %I:%M %p')

        cols_to_round = ['close_spy', 'open_spy', 'high_spy', 'low_spy']
        df[cols_to_round] = df[cols_to_round].round(2)


        self.data = df
    
    def show_data(self):
        return self.data.head()
    
    def calc_candle_strength(self, price_1, price_2):
        result = abs(price_1 - price_2)

        return result

    
    def backtest_orb(self):
        count = 0
       
        for date, group in self.data.groupby(self.data.index.date):
            print("")
            print("")
        
            orb_high = group["high_spy"].iloc[0]
            orb_low = group["low_spy"].iloc[0]
            print("-" * 50)
            print(f'{date} -- orb_high: {orb_high} and orb_low: {orb_low}')
            print("-" * 50)
            
            for i in range(len(group)):
                open_spy = group["open_spy"].iloc[i]
                high = group["high_spy"].iloc[i]
                low = group["low_spy"].iloc[i]
                close = group["close_spy"].iloc[i]
                current_date = group.index[i]
                yesterday = current_date - pd.Timedelta(days=1)
                prev_5 = current_date - pd.Timedelta(days=5)

                is_uptrend_conditions = [
                    open_spy > orb_high,
                    low <= orb_high,
                    close >= orb_high,
                    self.calc_candle_strength(high, close) < self.calc_candle_strength(open_spy, low)
                ]

                is_downtrend_conditions = [
                    open_spy < orb_low,
                    high >= orb_low,
                    close <= orb_low,
                    self.calc_candle_strength(high, close) > self.calc_candle_strength(open_spy, low)
                ]
                
                if yesterday in group.index and prev_5 in group.index:
                    if group.loc[yesterday, "close_spy"] > group.loc[prev_5, "close_spy"]:
                        if all(is_uptrend_conditions):
                            count += 1
                            print(f"{group.index[i]}, low: {low}, close: {close} - BUY")
                
                    elif group.loc[yesterday, "close_spy"] < group.loc[prev_5, "close_spy"]:
                        if all(is_downtrend_conditions):
                            count += 1
                            print(f"{group.index[i]}, low: {low}, close: {close} - SELL")
                    
                else:
                    if all(is_uptrend_conditions):
                        count += 1
                        print(f"{group.index[i]}, low: {low}, close: {close} - BUY")
                    
                    if all(is_downtrend_conditions):
                        count += 1
                        print(f"{group.index[i]}, low: {low}, close: {close} - SELL")

        print(count)

if __name__ == "__main__":
    bt = Backtesting(10,5)
    bt.get_data("SPY")
    # print(bt.show_data())
    # print(bt.data.dtypes)
    bt.backtest_orb()