import yfinance as yf
import pandas as pd
import pytz

class Backtesting:
    def __init__(self, trend: str, profit_target: int):
        self.trend = trend
        self.profit_target = profit_target
        self.data = None
        self.loss = 0
        self.win = 0
        self.num_of_trades = 0
    
    def get_data(self, ticker: str):
        spy_data = yf.download(ticker, period="60d", interval="5m")

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

                if self.trend.lower() == "up":
                    if all(is_uptrend_conditions):
                        count += 1
                        print(f"{group.index[i]}, low: {low}, close: {close} - BUY")
                        status = self.trade(close, low, self.profit_target, i, group)

                        if status:
                            print("You won this trade")
                            self.num_of_trades = 0
                            break
                        
                        else:
                            self.num_of_trades += 1
                            print("You loss")
                            if self.num_of_trades == 2:
                                self.num_of_trades = 0
                                break
                
                elif self.trend.lower() == "down":
                    if all(is_downtrend_conditions):
                        count += 1
                        print(f"{group.index[i]}, low: {low}, close: {close} - SELL")
                        status = self.trade(close, high, self.profit_target, i, group)

                        if status:
                            print("You won this trade")
                            self.num_of_trades = 0
                            break
                        
                        else:
                            self.num_of_trades += 1
                            print("You loss")
                            if self.num_of_trades == 2:
                                self.num_of_trades = 0
                                break

                            
                # if yesterday in group.index and prev_5 in group.index:
                #     if group.loc[yesterday, "close_spy"] > group.loc[prev_5, "close_spy"]:
                #         if all(is_uptrend_conditions):
                #             count += 1
                #             print(f"{group.index[i]}, low: {low}, close: {close} - BUY")
                
                #     elif group.loc[yesterday, "close_spy"] < group.loc[prev_5, "close_spy"]:
                #         if all(is_downtrend_conditions):
                #             count += 1
                #             print(f"{group.index[i]}, low: {low}, close: {close} - SELL")
                    
                # else:
                #     if all(is_uptrend_conditions):
                #         count += 1
                #         print(f"{group.index[i]}, low: {low}, close: {close} - BUY")
                    
                #     if all(is_downtrend_conditions):
                #         count += 1
                #         print(f"{group.index[i]}, low: {low}, close: {close} - SELL")

        print(f'Num_of_trades: {count}')
        print(f'Win: {self.win}')
        print(f'Lose: {self.loss}')
        print(f'Win_rate: {round((self.win / count) * 100, 0)}%')
    
    def trade(self, entry, stop_loss_price, target, index, group):

        stop_loss = abs(entry - stop_loss_price)

        for i in range(index + 1, len(group)):
            high = group["high_spy"].iloc[i]
            low = group["low_spy"].iloc[i]

            if self.trend.lower() == "up":
                if low <= stop_loss_price:
                    self.loss += 1
                    return False

                elif high <= ((stop_loss * target) + entry):
                    self.win += 1
                    return True
            
            elif self.trend.lower() == "down":
                if high >= stop_loss_price:
                    self.loss += 1
                    return False

                elif low <= (entry - (stop_loss * target)):
                    self.win += 1
                    return True

if __name__ == "__main__":
    bt = Backtesting("up", 2)
    bt.get_data("SPY")
    # print(bt.show_data())
    # print(bt.data.dtypes)
    bt.backtest_orb()