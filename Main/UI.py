import os, Process, Data
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
		clear()
		while self.running:
			self.help()
			if self.debug: print("main")
			action = str(input("|>")).lower()
			if action in self.actions:
				clear()
				self.actions[action]()
			else:
				clear()
				print("\n***Invalid input***\n")
		else: print("Exiting Project Gamma...")
	def help(self):
		L = []
		for key in self.actions.keys():
			L.append(key)
		print("Enter one of the following inputs:\n", L)
	def about(self):
		print("About")
	def portfolio(self):
		print("Portfolio")
	def terminal(self):
		print("Terminal")
		Term = Terminal()
		Term.run()
		
class Terminal(object):
		def __init__(self):
			self.inTerminal = True
		def __repr__(self):
			return "Use the terminal function to gather data on an equity or currency"
		def run(self):
			print("Type 'quit' to exit, 'clear' to refresh, or 'help' for commands")
			while self.inTerminal:
				action = input("|>")
				action = action.lower()
				if action == 'quit': break
				elif action == 'help': self.getInstructions()
				elif action == 'clear': clear()
				else:
					action = self.parseInput(action)
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
			print("returning to Main")
		def getInstructions(self):
			print("Enter the object type (Equity/Currency) followed by the symbol\nand one of the following commands.\n")
			eq = Data.Equity("NONE")
			curr = Data.Currency("NONE")
			print("Equities")
			for key, val in eq.info.items():
				print("| ",key, ": returns", val)
			print("\nCurrencies")
			for key, val in curr.info.items():
				print("| ",key, ": returns", val)
		def parseInput(self, words):
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
		
x = UI()
x.main()