import constants
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
from scipy.stats import pearsonr

plt.rcParams["font.family"] = "sans-serif"
print(plt.rcParams.keys())
plt.rcParams["font.sans-serif"] = "Avant Garde"

name = "Accent"
cmap = get_cmap(name)  # type: matplotlib.colors.ListedColormap
colors = cmap.colors*200  # type: list


languages = constants.get_all_language_pairs()
languages2 = list(sorted(list(set ( [l[0] for l in languages] + [l[1] for l in languages]))))
languages2.remove('uig')
languages2.remove('epo')

print(languages2)
#languages = [('ell','tur')]
demand1 = constants.read_economic_indicators(languages2, ind_type="Import", ind="Top 5 absolute")
demand2 = constants.read_economic_indicators(languages2, ind_type="Export", ind="Top 5 absolute")
all_bleus = constants.read_BLEUs()

languages = list(set(constants.get_languages_to_Eng() + constants.get_languages_from_Eng()))
all_populations = constants.read_noneng_populations()


populations = [all_populations[l] for l in languages]
paper_num = constants.read_number_of_papers()
internal_paper_num = constants.read_number_of_internal_papers()
#accuracy = [all_bleus[l,'eng'] for l in languages]
accuracy = [(all_bleus[l,'eng']+all_bleus['eng',l])/2 for l in languages]

papers_to_eng = [paper_num[l,'eng']+internal_paper_num[l, 'eng'] for l in languages]
papers = [paper_num[l,'eng']+internal_paper_num[l, 'eng']+paper_num['eng',l]+internal_paper_num['eng',l] for l in languages]
ec_dem1 = [(demand1[l,'eng']+demand1['eng',l])/1000.0 for l in languages]
ec_dem2 = [(demand2[l,'eng']+demand2['eng',l])/1000.0 for l in languages]

with open("economic_indicators_data/bilingual_indicators")

#rho1 = pearsonr(populations, papers_to_eng)
rho1 = pearsonr(populations, papers)
print(f"rho (pop,papers) = {rho1}")
#rho2 = pearsonr(ec_dem, papers_to_eng)
rho2 = pearsonr(ec_dem1, papers)
print(f"rho (ec_dem1,papers) = {rho2}")
rho3 = pearsonr(ec_dem2, papers)
print(f"rho (ec_dem2,papers) = {rho2}")
#rho3 = pearsonr(papers_to_eng, accuracy)
rho4 = pearsonr(papers, accuracy)
print(f"rho (papers,acc) = {rho3}")


fig, ax = plt.subplots(1,4, figsize=(10, 2))
#ax[0].scatter(populations, papers_to_eng)
ax[0].scatter(populations, papers, marker='o', s=20, facecolors='none', edgecolors='blue')
ax[0].set_xlabel("Non-English Speaking\nPopulation (millions)", fontsize=11)
ax[0].set_ylabel("#Papers", fontsize=11)
ax[0].text(0.85,0.9, f"ρ={rho1[0]:.2f}", ha='center', va='center', transform=ax[0].transAxes, fontsize=11, style='italic')
for i in range(len(populations)):
	lang = languages[i]
	if papers[i] > 25 or populations[i] > 250:
		if lang in 'slv,hrv'.split(','):
			ax[0].annotate(lang,(populations[i],papers[i]),textcoords="offset points",ha='center',fontweight='bold',xytext=(0,-10))
		elif lang in 'hin,ron'.split(','):
			ax[0].annotate(lang,(populations[i],papers[i]),textcoords="offset points",ha='center',fontweight='bold',xytext=(11,-3))
		elif lang in 'deu'.split(','):
			ax[0].annotate(lang,(populations[i],papers[i]),textcoords="offset points",ha='center',fontweight='bold',xytext=(13,-5))
		elif lang in 'cmn'.split(','):
			ax[0].annotate(lang,(populations[i],papers[i]),textcoords="offset points",ha='center',fontweight='bold',xytext=(-6,4))
		else:
			ax[0].annotate(lang,(populations[i],papers[i]),textcoords="offset points",ha='center',fontweight='bold',xytext=(0,4))


#ax[0].set_xscale("log")

#ax[1].scatter(ec_dem, papers_to_eng)
ax[1].scatter(ec_dem1, papers, marker='o', s=20, facecolors='none', edgecolors='blue')
ax[1].set_xlabel(f"Economic Indicators:\nImports ($1B) ", fontsize=11)
#ax[1].set_ylabel("#Papers", fontsize=11)
ax[1].text(0.85,0.9, f"ρ={rho2[0]:.2f}", ha='center', va='center', transform=ax[1].transAxes, fontsize=11, style='italic')
for i in range(len(ec_dem1)):
	lang = languages[i]
	if papers[i] > 25 or ec_dem1[i] > 400:
		if lang in 'slv,hrv'.split(','):
			ax[1].annotate(lang,(ec_dem1[i],papers[i]),textcoords="offset points",ha='center',fontweight='bold',xytext=(0,-10))
		elif lang in 'deu,jpn'.split(','):
			ax[1].annotate(lang,(ec_dem1[i],papers[i]),textcoords="offset points",ha='center',fontweight='bold',xytext=(13,-5))
		elif lang in 'cmn'.split(','):
			ax[1].annotate(lang,(ec_dem1[i],papers[i]),textcoords="offset points",ha='center',fontweight='bold',xytext=(14,-2.5))
		elif lang in 'spa'.split(','):
			ax[1].annotate(lang,(ec_dem1[i],papers[i]),textcoords="offset points",ha='center',fontweight='bold',xytext=(-4,4))
		elif lang in 'ron'.split(','):
			ax[1].annotate(lang,(ec_dem1[i],papers[i]),textcoords="offset points",ha='center',fontweight='bold',xytext=(2,4))
		elif lang in 'nld'.split(','):
			ax[1].annotate(lang,(ec_dem1[i],papers[i]),textcoords="offset points",ha='center',fontweight='bold',xytext=(-2,2))
		else:
			ax[1].annotate(lang,(ec_dem1[i],papers[i]),textcoords="offset points",ha='center',fontweight='bold',xytext=(0,4))

#ax[1].scatter(ec_dem, papers_to_eng)
ax[2].scatter(ec_dem2, papers, marker='o', s=20, facecolors='none', edgecolors='blue')
ax[2].set_xlabel(f"Economic Indicators:\nExports ($1B) ", fontsize=11)
#ax[2].set_ylabel("#Papers", fontsize=11)
ax[2].text(0.85,0.9, f"ρ={rho3[0]:.2f}", ha='center', va='center', transform=ax[2].transAxes, fontsize=11, style='italic')
for i in range(len(ec_dem2)):
	lang = languages[i]
	if papers[i] > 25 or ec_dem2[i] > 400:
		if lang in 'slv,hrv'.split(','):
			ax[2].annotate(lang,(ec_dem2[i],papers[i]),textcoords="offset points",ha='center',fontweight='bold',xytext=(0,-10))
		elif lang in 'deu,jpn'.split(','):
			ax[2].annotate(lang,(ec_dem2[i],papers[i]),textcoords="offset points",ha='center',fontweight='bold',xytext=(13,-5))
		elif lang in 'cmn'.split(','):
			ax[2].annotate(lang,(ec_dem2[i],papers[i]),textcoords="offset points",ha='center',fontweight='bold',xytext=(14,-2.5))
		elif lang in 'spa'.split(','):
			ax[2].annotate(lang,(ec_dem2[i],papers[i]),textcoords="offset points",ha='center',fontweight='bold',xytext=(-4,4))
		elif lang in 'ron'.split(','):
			ax[2].annotate(lang,(ec_dem2[i],papers[i]),textcoords="offset points",ha='center',fontweight='bold',xytext=(2,4))
		elif lang in 'nld'.split(','):
			ax[2].annotate(lang,(ec_dem2[i],papers[i]),textcoords="offset points",ha='center',fontweight='bold',xytext=(-2,2))
		else:
			ax[2].annotate(lang,(ec_dem2[i],papers[i]),textcoords="offset points",ha='center',fontweight='bold',xytext=(0,4))



#ax[2].scatter(papers_to_eng, accuracy)
ax[3].scatter(accuracy,papers, marker='o', s=20, facecolors='none', edgecolors='blue')
ax[3].set_xlabel("Utility (BLEU)", fontsize=11)
#ax[3].set_ylabel("#Papers", fontsize=11)
ax[3].text(0.15,0.9, f"ρ={rho4[0]:.2f}", ha='center', va='center', transform=ax[3].transAxes, fontsize=11, style='italic')
for i in range(len(accuracy)):
	lang = languages[i]
	if papers[i] > 25 or accuracy[i] > 44:
		if lang in 'slv,hrv'.split(','):
			ax[3].annotate(lang,(accuracy[i],papers[i]),textcoords="offset points",ha='center',fontweight='bold',xytext=(0,-10))
		elif lang in 'deu'.split(','):
			ax[3].annotate(lang,(accuracy[i],papers[i]),textcoords="offset points",ha='center',fontweight='bold',xytext=(2,-10))
		elif lang in 'cmn'.split(','):
			ax[3].annotate(lang,(accuracy[i],papers[i]),textcoords="offset points",ha='center',fontweight='bold',xytext=(4,2))
		else:
			ax[3].annotate(lang,(accuracy[i],papers[i]),textcoords="offset points",ha='center',fontweight='bold',xytext=(0,4))
from numpy.polynomial.polynomial import polyfit
# Fit with polyfit
b, m = polyfit(accuracy, papers, 1)
x = np.array([10,50])
ax[3].plot(x, b + m * x, '-', c='k', linewidth=2)
plt.tight_layout()
plt.subplots_adjust(wspace=0.2)
plt.show()

fig.savefig(f"figs/correlations_to_and_from_eng.pdf", quality=100, format='pdf')




N = 50
print(f"Number of papers: {paper_num}")
print("Pairs with the highest demand")
items = demand1.items()
for i,it in enumerate(reversed(sorted(items, key=lambda x:x[1])[-N:])):
	print(f"{i+1}\t{it[0][0]}\t{it[0][1]}\t{it[1]}\t{paper_num[it[0]]}")


