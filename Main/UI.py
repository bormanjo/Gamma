import os, Process, Data, getpass
from distutils.util import strtobool

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    
class UI(object):
    def __init__(self):
        self.running = True
        self.debug = True
        self.version = "Alpha 0.5"
        self.actions = {
                        "?":self.about,
                        "quit":exit,
                        "portfolio":self.portfolio,
                        "terminal":self.terminal,
                        }
    def __repr__(self):
        return "+---Welcome to Project Gamma---+/nVersion: "+ self.version+'\n'
    def main(self):
        '''Main function'''
        clear()
        while self.running:
            self.help()
            if self.debug: print("main")
            action = str(input("|> ")).lower()
            if action in self.actions:
                clear()
                self.actions[action]()
            else:
                clear()
                print("\n***Invalid input***\n")
        else: print("Exiting Project Gamma...")
    def help(self):
        '''Prints the options for the main menu'''
        L = []
        for key in self.actions.keys():
            L.append(key)
        print("Enter one of the following inputs:\n", L)
    def about(self):
        '''About the program'''
        print("About")
    def portfolio(self):
        '''Switches to Portfolio Management functionality'''
        print("Portfolio")
        name = self.logIn()
        if name == None:
            return
        Port = Portfolio(name)
        Port.run()
    def terminal(self):
        '''Switches to terminal functionality'''
        print("Terminal")
        Term = Terminal()
        Term.run()
    def logIn(self):
        '''Initiates user login assuming user is registered'''
        Logger = Data.Credentials()
        clear()
        while True:
            print("Would you like to login (L) or register (R)?")
            hasAccount = input("|> ")
            if hasAccount.lower() == 'l':
                clear()
                print('*'*10+'\n* SECURE *\n'+'*'*10+'\n')
                while not Logger.loggedIn:
                    username = input("Hit enter to return\nUsername:\n|> ")
                    if username == '': return None
                    password = getpass.getpass("Password:\n|> ")
                    if Logger.login(username, password):
                        return username
                    else:
                        print('*'*10+'\n* SECURE *\n'+'*'*10+'\n')
                        print("The username and password entered are not recognized")
            elif hasAccount.lower() == 'r':
                username = input("Enter a username\n|>")
                password = getpass.getpass("Enter a password\n|> ")
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
        self.running = True
        self.portOptions = {
                            "buy":self.buy,
                            "sell":self.sell,
                            "view":self.view
                            }
    def run(self):
        Term = Terminal()
        while self.running:
            print()
            action = input("|> ")
            action.lower()
            action = parseInput(action)         #action: ["Action (Buy/sell)", "Type", "Symbol", "Quantity"]
            try:
                if action[0] == 'quit':
                    print("Returning to Main Menu")
                    break
                elif action[0] == 'help': self.get_instructions()
                elif action[0] == 'clear': clear()
                elif action[0] in self.portOptions:
                    print("options")
                    self.portOptions[action[0]](action[1],action[2], action[3])
                else:
                    Term.retrieve(action)
            except IndexError:
                pass
                
    def get_instructions(self):
        '''Prints a List of possible commands'''
    def view(self, *args):
        '''Prints Portfolio'''
        print("Something")
        portData = self.Processor.get_portfolio()
        for key, data in portData.items():
            print(key,": ", data)
        print(portData)
    def buy(self, *args):
        '''Adds position in symbol to portfolio'''
        self.Processor.change_position(args[0],args[1],int(args[2]))
        print("Purchase of ", args[1], " successful.")
    def sell(self, *args):
        '''Adds position in symbol to portfolio'''
        self.Processor.change_position(args[0],args[1],-int(args[2]))
        print("Sale of ", args[1], " successful.")
        
class Terminal(object):
        def __init__(self):
            self.inTerminal = True
        def __repr__(self):
            return "Use the terminal function to gather data on an equity or currency"
        def run(self):
            '''Main terminal function'''
            print("Type 'quit' to exit, 'clear' to refresh, or 'help' for commands")
            while self.inTerminal:
                action = input("|>")
                action = action.lower()
                if action == 'quit': break
                elif action == 'help': self.get_instructions()
                elif action == 'clear': clear()
                else:
                    print(self.retrieve(parseInput(action)))
            print("returning to Main")
        def retrieve(self, action):
            '''Given a Command List, retrieves the specified data'''
            try:
                if action[0] == "equity":
                    symObj = Data.Equity(action[1])
                elif action[0] == "currency":
                    symObj = Data.Currency(action[1])                    
                print(action[2],": ", symObj.get_data(action[2]))
            except (KeyError, UnboundLocalError) as e:
                if e == KeyError:
                    print("The command ",action[2]," is not recognized for the symbol ", action[1])
                else:
                    print("The specified object type is invalid")
        def get_instructions(self):
            '''Prints a list of recognized commands for Equities and Currencies'''
            print("Enter the object type (Equity/Currency) followed by the symbol\nand one of the following commands.\n")
            eq = Data.Equity("NONE")
            curr = Data.Currency("NONE")
            print("Equities")
            for key, val in eq.info.items():
                print("| ",key, ": returns", val)
            print("\nCurrencies")
            for key, val in curr.info.items():
                print("| ",key, ": returns", val)
        
        
x = UI()
#x.main()
