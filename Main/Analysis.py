import Data
from datetime import date, timedelta



class Analyze(object):
    def __init__(self, Equity):
        '''Takes Equity object as parameter'''
        self.Equity = Equity
        self.yfVals = {}
        self.histValDescript = {"Date":"Values retrieved from this date",
                        "symbol":"Equity Symbol",
                        "high":"Day's high",
                        "low":"Day's low",
                        "open":"Opening price",
                        "close":"Closing price",
                        "adj_close":"Closing price accounting for corporate actions",
                        "volume":"Day's volume"
                        }
        self.today = date.today()
        self.lastTradeDay = self.getLastTradingDay()
        self.lastTradeDayStr = str(self.lastTradeDay)
        
        for key in Equity.data:
            self.yfVals[key] = Equity.get_data(key)
        for key in self.yfVals:
            print(key, ': ', self.yfVals[key])
    def getLastTradingDay(self):
        '''returns a datetime object of  the last trading day, must convert to string to use'''
        dateVar = self.today
        while True:
            last = (dateVar - timedelta(days=1))
            if self.get_historical(str(last)) != []: break
        return last
    def get_historical(self, d1, *d2):
        '''Returns the historical data for the time between d1 and d2, not including market close days
           Format: year-month-day'''
        if d2 == (): d2 = d1
        else: d2 = d2[0]
        print(d1,' ', d2)
        return self.Equity.equity.get_historical(d1,d2)
    def mov_avg_ratio(self):
        '''Returns the ratio of the 50 day moving average to the 200 day moving average'''
        return float(self.yfVals['mov_avg_50'])/float(self.yfVals['mov_avg_200'])
    def spreadHL_year(self):
        '''Returns the 52 week high/low spread'''
        return float(self.yfVals['high_52']) - float(self.yfVals['low_52'])
    def spreadHL_day(self):
        '''Returns the daily high/low spread'''
        return float(self.yfVals['high_day']) - float(self.yfVals['low_day'])
    def get_historical_val(self, val, d1, *d2):
        '''Returns a dictionary of values for the specified date or range'''
        D = {}
        if d2 == (): d2 = d1
        else: d2 = d2[0]
        L = self.get_historical(d1,d2)
        for dict in L:
            D[dict["Date"]] = dict[val]
        return D
    def intraday_change_percent(self):
        '''Returns percentage change between today and the last trading day'''
        pClose = float(self.get_historical_val("Close", self.lastTradeDayStr)[self.lastTradeDayStr])
        pToday = float(self.yfVals["price"])
        return round(((pToday - pClose)/pClose)*100, 4)

def test():
    A = Data.Equity('AAPL')
    B = Analyze(A)

    print(B.intraday_change_percent())
        
test()
