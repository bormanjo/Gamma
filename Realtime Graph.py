import sys
sys.path.append('/Users/jzmanrulz/anaconda/lib/python3.4/site-packages')
import matplotlib.pyplot as plt
import numpy as np
import time

fig = plt.figure()
ax = fig.add_subplot(111)

x = np.arange(10000)
y = np.random.randn(10000)

li, = ax.plot(x,y)

fig.canvas.draw()
plt.show()

while True:
    try:
        y[:-10] = y[10:]
        y[-10:] = np.random.randn(10)
        
        li.set_ydata(y)
        
        fig.canvas.draw()
        
        time.sleep(0.01)
    except KeyboardInterrupt:
        break
