import attributes

class Engine(object):
    def __init__(self):
        self.running = True
        self.version = 0.1
        self.actions = {
                    "?":self.Help,
                    "quit":exit,
                        }

    def __repr__(self):
        return "Welcome to Project Gamma Version " + str(self.version)
    
    def run(self):
        print("\n   Type '?' for a list of commands")
        while self.running:
            command = str(input("> "))
            if command in self.actions:
                self.actions[command]()
            else:
                instructions = self.parseInput(command)
                print(self.validateInput(instructions))
        else:
            print("Quitting...")
    def Help(self):
        '''returns a list of commands and their descriptions'''
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
                CL = [splitString(S)] + CL
                S = removeString(S, CL[0])
                if len(S) > 1 and S[0] == " ": S = S[1:]
            return CL[::-1]

        return commandList(words)

    def validateInput(self, L):
        '''given a list of commands L, validates that each element is a valid command'''
        newEquity = attributes.Equity(L[0])
        try:
            assert L[1] in newEquity.data
        except AssertionError:
            return "The command entered is not recognized.\nEnter help for a list of recognized commands"

        return newEquity.get_data( L[1])
            
    
x = Engine()
x.run()

