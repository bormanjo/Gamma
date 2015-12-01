import sys
sys.path.append(r'/Users/jzmanrulz/anaconda/lib/python3.4/site-packages')
import yahoo_finance as yf

helpDict = {
         "high_52":"the 52 week high",
         "low_52":"the 52 week low",
         "high_day":"the day's high",
         "low_day":"the day's low",
         "price":"the current price",
         "volume":"the current volume of outstanding shares",
         "market_cap":"total worth of all outstanding shares (price*volume)",
         "pe":"the price-per-share to earnings-per-share ratio",
         "peg":"the price-to-earnings-to-growth ratio",
         "pb":"the price-to-book ratio",
         "ps":"the price-to-sales ratio",
         "info":"the info about the symbol",
         "open":"the day's opening price",
         "exchange":"the exchange the symbol is listed on",
         "ebitda":"the earnings before interest, taxes, depreciation and amortization",
         "div_yield":"the dividend yield",
         "earnings":"the earnings per share",
         "mov_avg_50":"the 50 day simple moving average",
         "mov_avg_200":"the 200 day simple moving average",
            }


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
                     "mov_avg_200":self.equity.get_200day_moving_avg
                     }
    
    def get_data(self, value):
        return self.data[value]()


        






