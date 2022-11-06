import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

colors = sns.color_palette('pastel')
sns.set_style('darkgrid')
info40 = np.loadtxt('datafiles/info40.txt')
t = info40[4::5]
sort40 = np.sort(t)
sortedindex40 = []

for i in range(len(t)):
    sortedindex40.append(int(np.where(sort40[i] == t)[0]))

print(sortedindex40)
t = info40[4::5][sortedindex40]
ma40 = np.flip(np.sort(abs(info40[1::5])))
plt.plot(t, ma40)
plt.show()

"""
plt.plot(t, ma40, label = 'N = 40')
plt.show()
"""
"""
info60 = np.loadtxt('datafiles/info60.txt')
info80 = np.loadtxt('datafiles/info80.txt')
info100 = np.loadtxt('datafiles/info100.txt')

en40 = info40[::5]
ma40 = info40[1::5]
hc40 = info40[2::5]
sus40 = info40[3::5]

en60 = info60[::5]
ma60 = info60[1::5]
hc60 = info60[2::5]
sus60 = info60[3::5]

en80 = info80[::5]
ma80 = info80[1::5]
hc80 = info80[2::5]
sus80 = info80[3::5]

en100 = info100[::5]
ma100 = info100[1::5]
hc100 = info100[2::5]
sus100 = info100[3::5]
"""
"""
# Plotting energies.
plt.plot(t, en40, label = 'N = 40')
plt.plot(t, en60, color = '#EC5A46', label = 'N = 60')
plt.plot(t, en80, color = '#E7EC46', label = 'N = 80')
plt.plot(t, en100, color = '#E946EC', label = 'N = 100')
plt.xlabel('Temperatures [K]')
plt.ylabel('$<\epsilon>$ [J]')
plt.title('Averege energy per spin for different lattice sizes plotted against temperatures')
plt.legend()
plt.savefig('Averege energy per spin.pdf')
plt.plot()

# Plotting magnetization.
plt.plot(t, ma40, label = 'N = 40')
plt.plot(t, ma60, color = '#EC5A46', label = 'N = 60')
plt.plot(t, ma80, color = '#E7EC46', label = 'N = 80')
plt.plot(t, ma100, color = '#E946EC', label = 'N = 100')
plt.xlabel('Temperatures [K]')
plt.ylabel('$<|m|>$ [J]')
plt.title('Averege magnetization per spin for different lattice sizes plotted against temperatures')
plt.legend()
plt.savefig('Averege magnetization per spin.pdf')
plt.plot()

# Plotting heat-capacity.
plt.plot(t, ma80, label = 'N = 40')
plt.plot(t, ma60, color = '#EC5A46', label = 'N = 60')
plt.plot(t, ma80, color = '#E7EC46', label = 'N = 80')
plt.plot(t, ma100, color = '#E946EC', label = 'N = 100')
plt.xlabel('Temperatures [K]')
plt.ylabel('$<|m|>$ [J]')
plt.title('Specific heat capcity for different lattice sizes plotted against temperatures')
plt.legend()
plt.savefig('Spec heat capcity per spin.pdf')
plt.plot()
"""
