import attributes, json, time, os
from distutils.util import strtobool

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Engine(object):
    def __init__(self):
        self.running = True
        self.version = 0.1
        self.actions = {
                        "?":self.Help,
                        "quit":exit,
                        "portfolio":self.managePortfolio
                        }

    def __repr__(self):
        return "Welcome to Project Gamma Version " + str(self.version)
    
    def run(self):
        print("\n   Type '?' for help, 'portfolio' to invest, or 'quit' to exit")
        while self.running:
            command = str(input("> "))
            if command in self.actions:
                self.actions[command]()
            else:
                instructions = self.parseInput(command) #Add error check to parse
                print(self.validateInput(instructions))
        else:
            print("Quitting...")
    def Help(self):
        '''returns a list of commands and their descriptions'''
        clear()
        print("Enter the symbol followed by one of the following commands:","\n+","-"*12)
        for key, value in attributes.helpDict.items():
            print('| ', key, ': returns ', value)
        print("+", "-"*12)
    def parseInput(self, words):
        '''takes given string of words and outputs a list of each word in the string'''
        z = ""
        def splitString(y):
            if y == "" or y[0] == " ":
                return ""
            else:
                return y[0] + splitString(y[1:])
        def removeString(S, R):
            '''given strings S and R (assuming R is in S), returns S without R'''
            if R == "" or S == "":
                return S
            elif S[0] == " ":
                return removeString(S[1:], R)
            elif R[0] != S[0]:
                return S[0] + removeString(S[1:], R)
            else:
                return removeString(S[1:], R[1:])
        def commandList(S):
            '''given a string S of commands, returns a list of each word in command'''
            CL = []
            while len(S)>0:
                CL = [splitString(S)] + CL #add error check here, make sure list length is 2
                S = removeString(S, CL[0])
                if len(S) > 1 and S[0] == " ": S = S[1:]
            return CL[::-1]
        
        return commandList(words)

    def validateInput(self, L):
        '''given a list of commands L, validates that each element is a valid command, if so returns the associated value'''
        newEquity = attributes.Equity(L[0])
        try:
            assert L[1] in newEquity.data
        except AssertionError:
            clear()
            return "The command entered is not recognized.\nEnter help for a list of recognized commands"

        return newEquity.get_data( L[1])
        
    def managePortfolio(self):
        '''Main interface for buying and selling shares'''
        def readPortfolio():
            with open('portfolio.txt') as t:
                try:
                    data = json.load(t)
                except ValueError:
                    data = {}
            with open('portfolio.txt', 'r') as t:
                data = json.load(t)
                for d in data:
                    print(d)
                    try:
                        for key, value in data[d].items():
                            print(" "*4, key, ": ", value)
                    except AttributeError:
                        pass

        def writePortfolio(symbol, quantity, price, value, time):
            '''Writes given data values to a dictionary in portfolio.txt'''
            with open('portfolio.txt') as t:
                try:
                    portfolio = json.load(t)
                except ValueError:
                    portfolio = {}
            with open('portfolio.txt', 'w') as t:
                try:
                    portfolio[symbol]["Quantity"] += quantity
                    portfolio[symbol]["Transaction Price"] += [price]
                    portfolio[symbol]["Net Worth"] += value
                    portfolio[symbol]["Purchase Time"] += time
                except KeyError:
                    portfolio[symbol] = {"Quantity":quantity, "Buy Price":[price], "Net Worth":value, "Purchase Time":[time]}
                json.dump(portfolio, t)

        def purchase(sym, qty):
            '''given a string 'sym' and an int quantity 'qty', adds the purchase to portfolio'''
            newEquity = attributes.Equity(sym)
            qty = int(qty)
            pPrice = float(newEquity.data['price']())
            pValue = qty * pPrice
            prompt = "Would you like to buy " + sym + " for " + str(pPrice) + " at " + str(qty) + " shares?"
            confirm = strtobool(input(prompt))
            if confirm:
                writePortfolio(sym, qty, pPrice, pValue, time.time())
                print('$ ', qty, " shares of ", sym, " were purchased at ", pPrice, " for $", pValue)
            else:
                return
        def sell(sym, qty):
            '''given a string 'sym' and an int quantity 'qty', sells the sym from portfolio'''
            newEquity = attributes.Equity(sym)
            qty = int(qty)
            sPrice = float(newEquity.data['price']())
            sValue = qty * sPrice
            prompt = "Would you like to sell " + sym + " for " + str(sPrice), " at " + str(qty) + " shares?"
            confirm = strtobool(input(prompt))
            if confirm:
                writePortfolio(sym, -qty, sPrice, -sValue, time.time())
                print('$ ', qty, " shares of ", sym, " were sold at ", sPrice, " for $", sValue)
            else:
                return
        def getTrade(d):
            return input("Enter the symbol and quantity of shares you want to "+ d +"\n >")
        def test():
            """Tests whether a portfolio already exists, if not creates a new portfolio"""
            try:
                portfolio = open('portfolio.txt')
                portfolio.close
            except FileNotFoundError:
                portfolio = open('portfolio.txt', 'w+')
                print("No existing portfolio was found so a new portfolio was created")
                portfolio.close()
        test()
        
        while True:
            clear()
            decision = str(input("Would you like to 'buy,' 'sell,' 'close' or 'view' your portfolio? (Enter the word) \n >"))
            if decision.lower() == 'buy':
                B = self.parseInput(input())
                purchase(B[0], B[1])
            elif decision.lower() == 'sell':
                S = self.parseInput(getTrade(decision))
                sell(S[0], S[1])
            elif decision.lower() == 'view':
                readPortfolio()
            elif decision.lower() == 'close':
                break
            else: print('\nThat is not a valid entry. \n')
    
x = Engine()
x.run()

