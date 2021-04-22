import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle
from matplotlib.cm import get_cmap
from collections import defaultdict
from scipy.special import expit
from data import constants
from matplotlib.colors import ListedColormap,LinearSegmentedColormap

plt.rc('font', family='serif')
plt.rc('xtick', labelsize='x-small')
plt.rc('ytick', labelsize='x-small')


def gini(populations, accuracy):
    assert(len(populations) == len(accuracy))
    N = len(populations)
    sum_nom = 0
    sum_denom = 0
    for i in range(N):
        for j in range(N):
            sum_nom += populations[i] * populations[j] * np.abs(accuracy[i]-accuracy[j])
        sum_denom += populations[i]*accuracy[i]
    return sum_nom/(2*np.sum(populations)*sum_denom)


plt.rcParams["font.family"] = "sans-serif"
#print(plt.rcParams.keys())
plt.rcParams["font.sans-serif"] = "Avant Garde"


all_populations = constants.read_all_populations()

languages = constants.get_all_languages()

languages = [l for l in languages if l in all_populations]
populations = [all_populations[l] for l in languages]
counterfactual_accuracy_eng = [0 for l in languages if l != 'eng' else 1]

print(len(languages))
print(len(populations))
print(len(counterfactual_accuracy_eng))
print(sum(counterfactual_accuracy_eng))


def include_diversity(l, T=1):
    acc_arr = np.array(l)
    acc_arr = [f**T for f in acc_arr]
    N = sum(acc_arr)
    acc_arr = [f/N for f in acc_arr]
    return list(acc_arr)


accuracy = counterfactual_accuracy_eng

N = sum(populations)
metric1 = np.average([a for a,p in zip(accuracy,populations)])
metric2 = sum([a*p/N for a,p in zip(accuracy,populations)])

N = np.sum(populations)
old_populations = [p/N for p in populations]

#for temperature in [1, 0.5, 0.1]:
for temperature in [1,0.5,0.1]:

    populations = include_diversity(old_populations, T=temperature)

    print(f"Simple macro-averaged accuracy: {np.average(accuracy)}")
    gini_coeff = gini(np.array(populations)*N, accuracy)
    print(f"Gini Coefficient: {gini_coeff}")
    M = 0
    for p,u in zip(populations,accuracy):
        M += p*u
    print(f"Mu score: {M}")


    
