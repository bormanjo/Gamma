import Data
from datetime import datetime

class Portfolio(object):
    def __init__(self, name):
        self.name = name
        self.standardVals = ["price","high_52","low_52","high_day","low_day","pe"]
        self.Retriever = Data.DataIO()
        if self.name not in self.Retriever.portfolios():
            self.Retriever.write_portfolio(self.name)
            
    def __repr__(self):
        portData = self.Retriever.read_portfolio(self.name)
        string = ''
        for symbol in portData:
            string += str(symbol) + '\n'
            for item, val in portData[symbol].items():
                string += ("    " + str(item) + ': '+ str(val) + '\n')
        return string
    
    def change_position(self, obj, symbol, quantity):
        '''Adds or subtracts the a given amount from the portfolio
           [Total Equity, Quantity of shares, [Trade history], Type]
           [liquidVal,    quantity+position,  prevTrades,      obj ]
        '''
        #Setup Symbol's Skeleton Data Structure
        self.Retriever.write_symbol(self.name, symbol, obj)
        #Retrieve Values from Symbol
        liquidCash = float(self.Retriever.read_value(self.name, "_info", "Liquid Cash"))#Spendable Money
        price = float(self.Retriever.yf_value(obj, symbol, "price"))       
        liquidVal = float(self.Retriever.read_value(self.name, symbol, "Net Liquidity"))#Value of Trade
        position = int(self.Retriever.read_value(self.name, symbol, "Quantity"))        #Number of Shares owned 
        prevTrades = self.Retriever.read_value(self.name, symbol, "Trades")             #Trade History
        #Modify retrieved values based on input
        quantity = int(quantity)
        position += quantity
        liquidVal = price * quantity
        prevTrades += [[price, quantity, str(datetime.now())]]
        #Modify Spendable Cash
        self.Retriever.write_value(self.name, "_info", "Liquid Cash", float(liquidCash)-float(liquidVal))
        #Store Trade information and resulting portfolio
        for item, val in zip(self.Retriever.positionVals,[liquidVal+(price*quantity), position, prevTrades, obj]):
            print(item,' ',val)
            self.Retriever.write_value(self.name, symbol, item, val)
        
    def get_yf(self, obj, symbol):
        '''returns a dict of standard values for a given equity or currency'''
        values = {}
        for value in self.standardVals:
            values[value] = self.Retriever.yf_value(obj, symbol, value)
        return values
    def get_portfolio(self):
        """returns dictionary of data for all current positions in portfolio"""
        return self.Retriever.read_portfolio(self.name)

x = Portfolio("John")
x.change_position("Equity", "AAPL", 10)
