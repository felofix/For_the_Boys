import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import PercentFormatter

N = 20
colors = sns.color_palette('pastel')
sns.set_style('darkgrid')

T1data = np.loadtxt("datafiles/energies20x20_T1.txt")/N
T24data = np.loadtxt("datafiles/energies20x20_T24.txt")/N

h1 = sns.histplot(data=T1data, stat="probability",  bins = 500)
h1.set_xlabel('$\epsilon$')
plt.title('Normalized histogram of $\epsilon$ samples with T = 1 $J/k_B$')
plt.savefig('Normalized histogram T = 1 J.pdf')
plt.show()

h2 = sns.histplot(data=T24data, stat="probability",  bins = 500)
h2.set_xlabel('$\epsilon$')
plt.title('Normalized histogram of $\epsilon$ samples with T = 2.4 $J/k_B$')
plt.savefig('Normalized histogram T = 2.4 J.pdf')
plt.show()
