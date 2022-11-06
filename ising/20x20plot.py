import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def mean_epsilon(energies, N):
	return np.mean(energies/N)

def mean_mag(magnetizations, N):
	return np.mean(abs(magnetizations/N))

def equilibration_e(energies, N):
	mean_epsilons = np.zeros(len(energies))
	for i in range(1, len(mean_epsilons)):
		mean_epsilons[i] = mean_epsilon(energies[:i], N)
	return mean_epsilons

def equilibration_m(magnetizations, N):
	mean_mags = np.zeros(len(magnetizations))
	for i in range(1, len(mean_mags)):
		mean_mags[i] = mean_mag(magnetizations[:i], N)
	return mean_mags

# Energies.
energiesUT1 = np.loadtxt('datafiles/energies20x20_T1_UOrdered.txt')
energiesOT1 = np.loadtxt('datafiles/energies20x20_T1_Ordered.txt')
energiesUT24 = np.loadtxt('datafiles/energies20x20_T24_UOrdered.txt')
energiesOT24 = np.loadtxt('datafiles/energies20x20_T24_Ordered.txt')

# Magnetizations.
magnetUT1 = np.loadtxt('datafiles/magnetizations20x20_T1_UOrdered.txt')
magnetOT1 = np.loadtxt('datafiles/magnetizations20x20_T1_Ordered.txt')
magnetUT24 = np.loadtxt('datafiles/magnetizations20x20_T24_UOrdered.txt')
magnetOT24 = np.loadtxt('datafiles/magnetizations20x20_T24_Ordered.txt')

n20 = 400
three = 300000
cycles = np.linspace(0, len(energiesUT1), len(energiesUT1))
colors = sns.color_palette('pastel')
sns.set_style('darkgrid')

equiEUT1 = equilibration_e(energiesUT1, n20)
equiEOT1 = equilibration_e(energiesOT1, n20)
equiEUT24 = equilibration_e(energiesUT24, n20)
equiEOT24 = equilibration_e(energiesOT24, n20)

equiMUT1 = equilibration_m(magnetUT1, n20)
equiMOT1 = equilibration_m(magnetOT1, n20)
equiMUT24 = equilibration_m(magnetUT24, n20)
equiMOT24 = equilibration_m(magnetOT24, n20)


# Plotting equilibrium energies for T=1. 
plt.xlabel("Monte Carlo cycles")
plt.ylabel("$<\epsilon> [J]$")
plt.title("$<\epsilon>$ plotted against number of Monte Carlo cycles for N = 20x20 with T = 1 $J/k_B$")
plt.plot(cycles, equiEUT1, label='Unordered')
plt.plot(cycles, equiEOT1,color = '#EC5A46', label='Ordered')
plt.legend()
plt.savefig("Mean energy development for 20x20 with T = 1 J.pdf")
plt.show()

# Plotting equilibrium energies for T=2.4.
plt.xlabel("Monte Carlo cycles")
plt.ylabel("$<\epsilon> [J]$")
plt.title("$<\epsilon>$ plotted against number of Monte Carlo cycles for N = 20x20 with T = 2.4 $J/k_B$")
plt.plot(cycles, equiEUT24, label='Ordered')
plt.plot(cycles, equiEOT24,color = '#EC5A46', label='Unordered')
plt.legend()
plt.savefig("Mean energy development for 20x20 with T = 2.4 J.pdf")
plt.show()

# Plotting equilibrium magnetizations for T = 1
plt.xlabel("Monte Carlo cycles")
plt.ylabel("$<|m|>$")
plt.title("$<|m|>$ plotted against number of Monte Carlo cycles for N = 20x20 with T = 1 $J/k_B$")
plt.plot(cycles, equiMUT1, label='Unordered')
plt.plot(cycles, equiMOT1,color = '#EC5A46', label='Ordered')
plt.legend()
plt.savefig("Mean magnetization development for 20x20 with T = 1 J.pdf")
plt.show()

# Plotting equilibrium magnetizations for T = 1
plt.xlabel("Monte Carlo cycles")
plt.ylabel("$<|m|>$")
plt.title("$<|m|>$ plotted against number of Monte Carlo cycles for N = 20x20 with T = 2.4 $J/k_B$")
plt.plot(cycles, equiMUT24, label='Unordered')
plt.plot(cycles, equiMOT24,color = '#EC5A46', label='Ordered')
plt.legend()
plt.savefig("Mean magnetization development for 20x20 with T = 2.4 J.pdf")
plt.show()
