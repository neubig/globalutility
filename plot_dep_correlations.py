import constants
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpl_patches
from matplotlib.cm import get_cmap
from scipy.stats import pearsonr,spearmanr
from numpy.polynomial.polynomial import polyfit

corr_func = spearmanr

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = "Avant Garde"

name = "Accent"
cmap = get_cmap(name)  # type: matplotlib.colors.ListedColormap
colors = cmap.colors*200  # type: list


languages = constants.get_dep_languages()
languages2 = list(languages)

print(languages2)
demand1 = constants.read_gdp(languages2)
all_accs = constants.read_dep(system='udf')
all_populations = constants.read_dep_populations()
all_populations_L1 = constants.read_dep_populations(L1only=True)

try:
	languages.remove('uig')
	languages.remove('epo')
	languages.remove('nno')
except:
	pass



populations = [all_populations[l] for l in languages]
populations_L1 = [all_populations_L1[l] for l in languages]
NS = np.sum(populations)
NS_L1 = np.sum(populations_L1)

accuracy = [all_accs[l] for l in languages]
M = max(accuracy)
utility = [(all_accs[l]/M) for l in languages]

ec_dem1 = [demand1[l] for l in languages]

for i,l in enumerate(languages):
	print(l,populations[i], accuracy[i], ec_dem1[i])

rho1 = corr_func(populations, utility)
print(f"rho (pop,utility) = {rho1}")
rho1l1 = corr_func(populations_L1, utility)
print(f"rho (popL1,utility) = {rho1}")
rho2 = corr_func(ec_dem1, utility)
print(f"rho (ec_dem1,utility) = {rho2}")


fig, ax = plt.subplots(1,3, figsize=(10, 2))
ax[0].scatter(populations, utility, marker='o', s=10, facecolors='none', edgecolors='blue')
ax[0].set_xlabel("Population (millions)", fontsize=11)
ax[0].set_ylabel("Per-Person Utility", fontsize=11)
mmax = max(populations)
for i in range(len(populations)):
	lang = languages[i]
	if utility[i] < 0.1:
		ax[0].annotate(lang,(populations[i],utility[i]),textcoords="offset points",ha='center',fontweight='bold',xytext=(0,4))
p3 = np.poly1d(np.polyfit(populations, utility, 2))
x = np.linspace(min(populations), max(populations), 1000)
ax[0].plot(x, p3(x), '-', c='blue', alpha=0.3, linewidth=10)
handles = [mpl_patches.Rectangle((0, 0), 1, 1, fc="white", ec="white", lw=0, alpha=0)]
labels = [f"ρ={rho1[0]:.2f}"]
ax[0].legend(handles, labels, loc='best', fontsize=11, fancybox=True, framealpha=0.7,  handlelength=0, handletextpad=0)
ax[0].set_xscale('log')

ax[1].scatter(populations_L1, utility, marker='o', s=10, facecolors='none', edgecolors='blue')
ax[1].set_xlabel("Population (L1 only, millions)", fontsize=11)
mmax = max(populations_L1)
for i in range(len(populations_L1)):
	lang = languages[i]
	if utility[i] > 1.0:
		ax[1].annotate(lang,(populations_L1[i],utility[i]),textcoords="offset points",ha='center',fontweight='bold',xytext=(0,4))
p3 = np.poly1d(np.polyfit(populations_L1, utility, 2))
x = np.linspace(min(populations_L1), max(populations_L1), 1000)
ax[1].plot(x, p3(x), '-', c='blue', alpha=0.3, linewidth=10)
handles = [mpl_patches.Rectangle((0, 0), 1, 1, fc="white", ec="white", lw=0, alpha=0)]
labels = [f"ρ={rho1l1[0]:.2f}"]
ax[1].legend(handles, labels, loc='best', fontsize=11, fancybox=True, framealpha=0.7,  handlelength=0, handletextpad=0)
ax[1].set_xscale('log')

ax[2].scatter(ec_dem1, utility, marker='o', s=10, facecolors='none', edgecolors='blue')
ax[2].set_xlabel(f"Economic Indicators:\nGDP ($1M) ", fontsize=11)
mmax = max(ec_dem1)*0.3
for i in range(len(ec_dem1)):
	lang = languages[i]
	if utility[i] > 1.0:
		ax[2].annotate(lang,(ec_dem1[i],utility[i]),textcoords="offset points",ha='center',fontweight='bold',xytext=(0,4))
p3 = np.poly1d(np.polyfit(ec_dem1, utility, 2))
x = np.linspace(min(ec_dem1), max(ec_dem1), 1000)
ax[2].plot(x, p3(x), '-', c='blue', alpha=0.3, linewidth=10)
handles = [mpl_patches.Rectangle((0, 0), 1, 1, fc="white", ec="white", lw=0, alpha=0)]
labels = [f"ρ={rho2[0]:.2f}"]
ax[2].legend(handles, labels, loc='best', fontsize=11, fancybox=True, framealpha=0.7,  handlelength=0, handletextpad=0)
ax[2].set_xscale('log')

plt.tight_layout()
plt.subplots_adjust(wspace=0.2)
plt.show()

fig.savefig(f"figs/dep_correlations.pdf", quality=100, format='pdf')
