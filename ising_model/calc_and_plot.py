import numpy as np
import matplotlib.pyplot as plt

def mean_epsilon(energies, N):
	return np.mean(energies/N)

def mean_mag(magnetizations, N):
	return np.mean(abs(magnetizations/N))

def spes_heat_cap(energies, N, B, T):
	return (1/N)*(B/T)*np.var(energies)

def suceptibility(magnetizations, N, B, T):
	return (1/N)*(B)*np.var(magnetizations)

def equilibration_e(energies, N):
	mean_epsilons = np.zeros(len(energies))
	for i in range(1, len(mean_epsilons)):
		print(i)
		mean_epsilons[i] = mean_epsilon(energies[:i], N)
	return mean_epsilons

def equilibration_m(magnetizations, N):
	mean_mags = np.zeros(len(magnetizations))
	for i in range(1, len(mean_mags)):
		mean_mags[i] = mean_mag(magnetizations[:i], N)
	return mean_mags

jumpvalues = 3 # Values to ignore in datafiles. 
energies1 = np.loadtxt('datafiles/magnetizations2.100000.txt')
energies2 = np.loadtxt('datafiles/magnetizations2.133333.txt')
energies3 = np.loadtxt('datafiles/magnetizations2.166667.txt')
energies4 = np.loadtxt('datafiles/magnetizations2.200000.txt')
energies5 = np.loadtxt('datafiles/magnetizations2.233333.txt')
energies6 = np.loadtxt('datafiles/magnetizations2.266667.txt')
energies7 = np.loadtxt('datafiles/magnetizations2.300000.txt')
energies8 = np.loadtxt('datafiles/magnetizations2.333333.txt')
energies9 = np.loadtxt('datafiles/magnetizations2.366667.txt')
energies10 = np.loadtxt('datafiles/magnetizations2.400000.txt')
m1 = mean_epsilon(energies1[jumpvalues:], 20)
m2  = mean_epsilon(energies2[jumpvalues:], 20)
m3 = mean_epsilon(energies3[jumpvalues:],20)
m4 = mean_epsilon(energies4[jumpvalues:],20)
m5 = mean_epsilon(energies5[jumpvalues:],20)
m6 = mean_epsilon(energies6[jumpvalues:],20)
m7 = mean_epsilon(energies7[jumpvalues:],20)
m8 = mean_epsilon(energies8[jumpvalues:],20)
m9 = mean_epsilon(energies9[jumpvalues:],20)
m10 = mean_epsilon(energies10[jumpvalues:],20)
temps = np.array([2.1, 2.133, 2.167,2.2, 2.233, 2.267, 2.3, 2.33, 2.367, 2.4])
means = np.array([m1, m2, m3, m4, m5, m6, m7, m8, m9, m10])
plt.plot(temps, means)
plt.show()
