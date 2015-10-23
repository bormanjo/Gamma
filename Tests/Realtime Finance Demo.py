import matplotlib, math, random
import yahoo_finance as yf
from matplotlib import pylab
from pylab import *

xbounds = range(0,100,1)
ybounds = [0]*100

#pull info from yahoo finance for given ticker
ticker = "GOOG"
stock = yf.Share(ticker)
high = float(stock.get_days_high())
low = float(stock.get_days_low())


fig = pylab.figure(1)						#figures contain all plot elements, ie the entire graph
ax = fig.add_subplot(111)					#sub plots are the graphed objects, ax is a subplot
ax.grid(True)
ax.set_title("Stock Price (Realitme)")
ax.set_xlabel("time")
ax.set_ylabel("price")
ax.axis([0,100,high,low])
Stock1 = ax.plot(xbounds,ybounds,'-')

manager = pylab.get_current_fig_manager()

print(stock.get_open())

values = ([0]*99)+[float(stock.get_open())]

def prices(arg):
	global values
	
	stock.refresh()
	values.append(float(stock.get_price()))
	
def RealtimePloter(arg):
	global values
	#current x axis (cxa) is the length of values from max length to length-100
	cxa = range(len(values)-100,len(values),1)
	Stock1[0].set_data(cxa,pylab.array(values[-100:]))
	ax.axis([min(cxa),max(cxa),high,low])
	manager.canvas.draw()
	
timer = fig.canvas.new_timer(interval=20)	#Pylabs builtin event manager, loops ever 20 ms
timer.add_callback(RealtimePloter,())		#Realtime is executed every 20ms in the timer
timer2 = fig.canvas.new_timer(interval=20)
timer2.add_callback(prices,())
timer.start()
timer2.start()

pylab.show()