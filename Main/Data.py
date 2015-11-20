import json, sys
sys.path.append(r'/Users/jzmanrulz/anaconda/lib/python3.4/site-packages')
import yahoo_finance as yf

class Equity(object):
    def __init__(self, symbol):
        self.equity = yf.Share(symbol)
        self.data = {
            "high_52":self.equity.get_year_high,
            "low_52":self.equity.get_year_low,
            "high_day":self.equity.get_days_high,
            "low_day":self.equity.get_days_low,
            "price":self.equity.get_price,
            "volume":self.equity.get_volume,
            "market_cap":self.equity.get_market_cap,
            "pe":self.equity.get_price_earnings_ratio,
            "peg":self.equity.get_price_earnings_growth_ratio,
            "pb":self.equity.get_price_book,
            "ps":self.equity.get_price_sales,
            "info":self.equity.get_info,
            "open":self.equity.get_open,
            "exchange":self.equity.get_stock_exchange,
            "ebitda":self.equity.get_ebitda,
            "div_yield":self.equity.get_dividend_yield,
            "earnings":self.equity.get_earnings_share,
            "mov_avg_50":self.equity.get_50day_moving_avg,
            "mov_avg_200":self.equity.get_200day_moving_avg,
            "refresh":self.equity.refresh
            }
    def get_data(self, value):
        '''returns the specified data from YahooFinance'''
        return self.data[value]()
        
class Currency(object):
    def __init__(self, symbol):
        self.currency = yf.Currency(symbol)
        self.data = {
            "bid":self.currency.get_bid,
            "ask":self.currency.get_ask,
            "rate":self.currency.get_rate,
            "trade_time":self.currency.get_trade_datetime,
            "refresh":self.currency.refresh
            }
    def get_data(self, value):
        '''returns the specified data from YahooFinance'''
        return self.data[value]()

class DataIO(object):
	def __init__(self):
		self.positionVals = ["Net Liquidity","quantity", "trades", "type"]
    def yf_value(self, obj, symbol, value):
        '''Returns specified value for symbol from YahooFinance API'''
        if obj == "equity":
            A = Equity(symbol)
        elif obj == "currency":
            A = Currency(symbol)
        else:
            return "Invalid command"
        A.get_data("refresh")
        return A.get_data(value)
    def read_value(self, portfolio, symbol, value):
        '''Returns a specific value from the portfolio'''
        with open('portfolios.txt') as file:
            try:
                data = json.load(file)
            except ValueError:
                data = {}
            try:
                return data[portfolio][symbol][value] 
            except KeyError:
                return "No value exists in " + portfolio + " for the data specified"
    def write_value(self, portfolio, symbol, item, value):
        '''Writes the given data in specified portfolio'''
        with open('portfolios.txt', 'w+') as file:
            data = json.load(file)
            if portfolio not in data:
                data[portfolio] = {}                #create new portfolio in data
            if symbol not in data[portfolio]:
                data[portfolio][symbol] = {}        #create new symbol in portfolio
                
            data[portfolio][symbol][item] = value   #add value to item
            json.dump(data, file)
    def read_portfolio(self, portfolio):
        '''Returns current portfolio data'''
        with open('portfolios.txt') as file:
            data = json.load(file)
            try:
                data[portfolio]
            except KeyError:
                print("No portfolio of name '" + portfolio + "' found. Creating portfolio...")
                self.write_portfolio(portfolio)
            return data[portfolio]
    def write_portfolio(self, name):
        '''Writes a new portfolio'''
        with open("portfolios.txt", 'w+') as file:
            try:
                data = json.load(file)
            except ValueError:
                data = {}
            data[name] = {}
            json.dump(data, file)
            print("Portfolio: '", name, "' created.")


