import numpy as np
import re
import matplotlib.pyplot as plt
direc = "/Users/Felix/desktop/poisson.txt"

def read(direc):
	s = ""
	f = open(direc, "r")
	for line in f:
		s += line
	f.close
	return s

def createdata(datastring):

	xvalues = (datastring[:-1:2]) # creatse list of strings x values. 
	yvalues = (datastring[1::2]) # creatse list of strings y values.
	for i in range(len(xvalues)):
		xvalues[i] = float(xvalues[i])
		yvalues[i] = float(yvalues[i])

	return xvalues, yvalues

data = re.split('\n| ',read(direc))
xval, yval = createdata(data)

plt.plot(xval, yval)
plt.xlabel("x")
plt.ylabel("u(x)")
plt.show()


