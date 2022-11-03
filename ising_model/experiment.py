import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython import display

data = np.loadtxt("datafiles/matrixT1.txt")

#N = 20

"""
def update(i):
    print(i)
    ax.imshow(data[:][i*N:i*N + N])
    ax.set_axis_off()
    
fig, ax = plt.subplots()
anim = FuncAnimation(fig, update, frames=100, interval=1)
"""
#plt.hist(data, bins = 500)
plt.imshow(data)
plt.show()

