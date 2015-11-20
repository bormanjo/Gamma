import Data, time

class Portfolio(object):
    def __init__(self, name):
        self.name = name
        self.standardVals = ["price","high_52","low_52","high_day","low_day","pe"]

        self.retriever = Data.DataIO()
        self.retriever.read_portfolio(self.name)        #creates new portfolio if nonexistant
                                                        #need to add function to explicitly check
                                                        #currently returns data when it doesnt need to
		self.liquidCash = self.retriever.read_value(self.name, "_info", "liqCash")
		if self.liquidCash != type(int):
			self.liquidCash = 10000.00
			self.retriever.write_value(self.name, "_info", "liqCash", self.liquidCash)
			print("A default amount of ", self.liquidCash, " has been depositied into your account.")
		else:
			print("You have ", self.liquidCash, " available to invest.")
    def change_position(self, obj, symbol, quantity):
        '''Adds or subtracts the a given amount from the portfolio'''
        price = self.retriever.yf_value(obj, symbol, "price")

        try:
            x = self.retriever.read_value(self.name, symbol, "trades")
            print(x)
            tradeHistory = x
            position = self.retriever.read_value(self.name, symbol, "quantity")
        except KeyError:
            position = 0
            tradeHistory = []
            position += quantity
		liquidVal = price * quantity
        tradeHistory += [[price, quantity, time.time()]]
        for item in self.retriever.positionVals:
            for val in [liquidVal, quantity, tradeHistory, obj]:
                self.retriever.write_value(self.name, symbol, item, val)
        
    def get_yf(self, obj, symbol):
        '''returns a dict of data essential data for a given equity or currency'''
        values = {}
        for value in self.standardVals:
            values[value] = self.retriever.yf_value(obj, symbol, value)
        return values
    def get_portfolio(self):
        """returns all current positions in portfolio"""
        self.retriever.read_portfolio(self.name)

