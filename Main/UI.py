import os, Process, Data, getpass
from distutils.util import strtobool

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

debug = False

class UI(object):
    def __init__(self):
        self.running = True
        self.version = "Beta 1.0"
        self.actions = {
                        "about":self.about,
                        "quit":exit,
                        "portfolio":self.portfolio,
                        "terminal":self.terminal,
                        }
    def __repr__(self):
        return "+---Welcome to Project Gamma---+ \nVersion: "+ self.version + '\n \n'
    def main(self):
        '''Main function'''
        print(self)
        clear()
        while self.running:
            self.help()
            if debug: print("$Main")
            action = str(input("|> ")).lower()
            if action in self.actions:
                clear()
                self.actions[action]()
            else:
                clear()
                print("\n***Invalid input***\n")
        else: print("Exiting Project Gamma...")
    def help(self):
        '''Prints main menu options'''
        L = []
        for key in self.actions.keys():
            L.append(key)
        print("Enter one of the following inputs:\n", L)
    def about(self):
        '''About the program'''
        if debug: print("$About")
    def portfolio(self):
        '''Switch to Portfolio Management functionality'''
        if debug: print("$Go to Portfolio")
        name = self.logIn()
        if name == None:
            return
        Port = Portfolio(name)
        Port.run()
    def terminal(self):
        '''Switch to terminal functionality'''
        if debug: print("$Go to Terminal")
        Term = Terminal()
        Term.run()       
    def logIn(self):
        '''Initiates user login assuming user is registered'''
        if debug: print('$LogIn')
        Logger = Data.Credentials()
        clear()
        while True:
            print("Would you like to login (L) or register (R)?")
            account = input("|> ")
            if account.lower() == 'l':
                clear()
                print('*'*10+'\n* SECURE *\n'+'*'*10+'\n')
                while not Logger.loggedIn:
                    username = input("Hit enter to return\nUsername:\n|> ")
                    if username == '': return None
                    password = getpass.getpass("Password:\n|> ")
                    if Logger.login(username, password):
                        clear()
                        return username
                    else:
                        clear()
                        print('*'*10+'\n* SECURE *\n'+'*'*10+'\n')
                        print("The username and password entered are not recognized")
            elif account.lower() == 'r':
                username = input("Enter a username\n|>")
                password = getpass.getpass("Enter a password\n|> ")
                Logger.register(username, password)
            else:
                clear()
                print("Invalid Entry")
                

def parseInput(words):
    '''Parses over a given string of words and returns a list of the words'''
    def splitString(str):
        '''returns the string of characters up until the first space in a given string'''
        if str == "" or str[0] == " ":
            return ""
        else:
            return str[0] + splitString(str[1:])
    def removeString(S, R):
        '''Removes the first occurance of string R from S'''
        if S == "" or R == "":
            return S
        elif S[0] == " ":
            return removeString(S[1:], R)
        elif R[0] != S[0]:
            return S[0] + removeString(S[1:], R)
        else:
            return removeString(S[1:], R[1:])
    def commandList(S):
        '''Parses over a string S and returns a list of commands between spaces in given string'''
        CL = []
        while len(S) > 0:
            CL = [splitString(S)] + CL
            S = removeString(S, CL[0])
            if len(S) > 1 and S[0] == " ": S = S[1:]
        return CL[::-1]
    return commandList(words)
            
class Portfolio(object):
    def __init__(self, name):
        self.name = name
        self.Processor = Process.Process(name)
        self.inPortfolio = True
        self.options = {
                            "buy":self.buy,
                            "sell":self.sell,
                            }
        self.errorDict = {
                            1:"Input Validated",
                            -1:"Invalid Transaction type, must be 'Buy' or 'Sell'",
                            -2:"Invalid object type, must be 'Equity' or 'Currency'",
                            -3:"Invalid Symbol/Ticker",
                            -4:"Invalid quantity, must be positive integer"
                            }
    def run(self):
        '''Initiates Portfolio Management process'''
        if debug: print("$Portfolio")
        Term = Terminal()
        while self.inPortfolio:
            print()
            action = input("|> ")
            action.lower()
            action = parseInput(action)         #action: ["Action (Buy/sell)", "Type", "Symbol", "Quantity"]
            try:
                if action[0] == 'quit':
                    print("Returning to Main Menu")
                    self.inPortfolio = False
                elif action[0] == 'help': self.get_instructions()
                elif action[0] == 'clear': clear()
                elif action[0] == 'view': self.view()
                elif action[0] in self.options:
                    validation = self.validate_input(action[0],action[1],action[2],action[3])
                    print(self.errorDict[validation])
                    if validation == 1:
                        self.options[action[0]](action[1],action[2],action[3])
                else:
                    Term.get_action(action)
            except IndexError:
                print("Invalid Action")               
    def get_instructions(self):
        '''Prints a List of possible commands'''
        if debug: print("$Get Instructions")
        clear()
        print('*'*8+'\n* Help *\n'+'*'*8)
        print("Commands are structured as such:\n|> [Action] [Object Type] [Symbol] [Quantity]\n")
        print("For example:\n|> Buy Equity SYM 10\n Will purchase 10 shares of the equity\n")
        print("Actions:\n    'buy'\n    'sell'\nSingle Parameter Actions:")
        for i in ["'quit' - exits Portfolio Management", "'help' - get instructions", "'clear' - clear terminal", "'view' - view portfolio"]:
            print("   ",i)
        print("Object Type:\n    'Equity'\n    'Currency'")
        print("Symbol:\n     Enter any valid Equity/Currency Symbol\nQuantity:\n     Enter a positive integer value")
    def validate_input(self, transaction, obj, sym, qty):
        '''Returns True or False if input is valid'''
        if transaction not in {"buy", "sell"}: return -1
        elif obj not in {"equity", "currency"}: return -2
        elif self.Processor.test(obj, sym) == None: return -3
        elif int(qty) < 0: return -4
        else: return 1
    def view(self):
        '''Prints Portfolio'''
        if debug: print("$View Portfolio")
        portData = self.Processor.get_portfolio()
        for sym, data in portData.items():
            print(sym,": ")
            for item, val in data.items():
                print("     ", item, ": ", val)
    def buy(self, *args):
        if debug: print("$Buy")
        '''Adds position in symbol to portfolio'''
        tradeValue = self.Processor.change_position(args[0],args[1],int(args[2]))
        if tradeValue == -1: print("Insufficient funds. Trade Unsuccessful")
        elif tradeValue != None: print("Purchase of ", args[1].upper(), " successful for: $", tradeValue)
        else: print("Trade Unsuccessful")
    def sell(self, *args):
        if debug: print("$Sell")
        '''Adds position in symbol to portfolio'''
        tradeValue = self.Processor.change_position(args[0],args[1],-int(args[2]))
        if tradeValue != None: print("Sale of ", args[1].upper(), " successful for: $", tradeValue)
        else: print("Trade Unsuccessful")
    
class Terminal(object):
        def __init__(self):
            self.inTerminal = True
        def __repr__(self):
            return "Use the terminal function to gather data on an equity or currency"
        def run(self):
            '''Main terminal function'''
            if debug: print("$Terminal")
            print("Type 'quit' to exit, 'clear' to refresh, or 'help' for commands")
            while self.inTerminal:
                action = input("|>")
                action = action.lower()
                if action == 'quit':
                    print("Returning to Main Menu")
                    inTerminal = False
                    break
                elif action == 'help': self.get_instructions()
                elif action == 'clear': clear()
                else:
                    print(self.get_action(parseInput(action)))
        def get_action(self, action):
            '''Given a Command List, retrieves the specified data'''
            try:
                if action[0] == "equity":
                    symObj = Data.Equity(action[1])
                elif action[0] == "currency":
                    symObj = Data.Currency(action[1])                    
                print(action[2],": ", symObj.get_data(action[2]))
            except (KeyError, UnboundLocalError, IndexError) as e:
                if e == KeyError:
                    print("The command ",action[2]," is not recognized for the symbol ", action[1])
                else:
                    print("The command ", action," is not recognized")
        def get_instructions(self):
            '''Prints a list of recognized commands for Equities and Currencies'''
            if debug: print("$Get Instructions")
            print("Enter the object type (Equity/Currency) followed by the symbol\nand one of the following commands.\n")
            eq = Data.Equity("NONE")
            curr = Data.Currency("NONE")
            print("Equities")
            for key, val in eq.info.items():
                print("| ",key, ": returns", val)
            print("\nCurrencies")
            for key, val in curr.info.items():
                print("| ",key, ": returns", val)
        

if __name__ == "__main__":
    start = UI()
    start.main()
