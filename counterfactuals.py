import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle
from matplotlib.cm import get_cmap
from collections import defaultdict
from scipy.special import expit
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import constants

plt.rc("font", family="serif")
plt.rc("xtick", labelsize="x-small")
plt.rc("ytick", labelsize="x-small")


def gini(populations, accuracy):
    assert len(populations) == len(accuracy)
    N = len(populations)
    sum_nom = 0
    sum_denom = 0
    for i in range(N):
        for j in range(N):
            sum_nom += (
                populations[i] * populations[j] * np.abs(accuracy[i] - accuracy[j])
            )
        sum_denom += populations[i] * accuracy[i]
    return sum_nom / (2 * np.sum(populations) * sum_denom)


plt.rcParams["font.family"] = "sans-serif"
# print(plt.rcParams.keys())
plt.rcParams["font.sans-serif"] = "Avant Garde"


all_populations = constants.read_all_populations()

languages = constants.get_all_languages()

languages = [l for l in languages if l in all_populations]
populations = [all_populations[l] for l in languages]
counterfactual_accuracy_eng = [0 if (l != "eng") else 1 for l in languages]
counterfactual_accuracy_cmn = [0 if (l != "cmn") else 1 for l in languages]
counterfactual_accuracy_spa = [0 if (l != "spa") else 1 for l in languages]
counterfactual_accuracy_fra = [0 if (l != "fra") else 1 for l in languages]

"""
print(len(languages))
print(len(populations))
print(len(counterfactual_accuracy_eng))
print(sum(counterfactual_accuracy_eng))
print(len(counterfactual_accuracy_cmn))
print(sum(counterfactual_accuracy_cmn))
print(len(counterfactual_accuracy_spa))
print(sum(counterfactual_accuracy_spa))
print(len(counterfactual_accuracy_fra))
print(sum(counterfactual_accuracy_fra))
"""

inds = np.flip(np.argsort(populations))
ordered_populations = [populations[i] for i in inds]

"""
counterfactual_accuracy_linpop = np.linspace(0, 1, num=len(languages))


N = np.sum(populations)
counterfactual_accuracy_largepop = []
counterfactual_accuracy_smallpop = []
tempsum = 0
for i in inds:
    if tempsum < 0.5*N:
        counterfactual_accuracy_largepop.append(0)
        counterfactual_accuracy_smallpop.append(1)
    else:
        counterfactual_accuracy_largepop.append(1)
        counterfactual_accuracy_smallpop.append(0)
    tempsum += populations[i]

print(inds[:10])
print(ordered_populations[:10])
print(counterfactual_accuracy_linpop[:10])
print(counterfactual_accuracy_smallpop[:10])
print(counterfactual_accuracy_largepop[:10])

print(inds[-10:])
print(ordered_populations[-10:])
print(counterfactual_accuracy_linpop[-10:])
print(counterfactual_accuracy_smallpop[-10:])
print(counterfactual_accuracy_largepop[-10:])
print(len(counterfactual_accuracy_smallpop))
print(sum(counterfactual_accuracy_smallpop))
print(len(counterfactual_accuracy_largepop))
print(sum(counterfactual_accuracy_largepop))
print(N)


def include_diversity(l, T=1):
    acc_arr = np.array(l)
    acc_arr = [f**T for f in acc_arr]
    N = sum(acc_arr)
    acc_arr = [f/N for f in acc_arr]
    return list(acc_arr)

N = np.sum(populations)
old_populations = [p/N for p in populations]
old_ordered_populations = [p/N for p in ordered_populations]


print("counterfactual_accuracy_eng")
accuracy = counterfactual_accuracy_eng
for temperature in [1,0.1]:
    populations = include_diversity(old_populations, T=temperature)
    print(f"  Tau = {temperature}")
    M = 0
    for p,u in zip(populations,accuracy):
        M += p*u
    print(f"\tMu score: {M}")
    print(f"\tSimple macro-averaged accuracy: {np.average(accuracy)}")
    gini_coeff = gini(np.array(populations)*N, accuracy)
    print(f"\tGini Coefficient: {gini_coeff}")

print("counterfactual_accuracy_cmn")
accuracy = counterfactual_accuracy_cmn
for temperature in [1,0.1]:
    populations = include_diversity(old_populations, T=temperature)
    print(f"  Tau = {temperature}")
    M = 0
    for p,u in zip(populations,accuracy):
        M += p*u
    print(f"\tMu score: {M}")
    print(f"\tSimple macro-averaged accuracy: {np.average(accuracy)}")
    gini_coeff = gini(np.array(populations)*N, accuracy)
    print(f"\tGini Coefficient: {gini_coeff}")
    


print("counterfactual_accuracy_fra")
accuracy = counterfactual_accuracy_fra
for temperature in [1,0.1]:
    populations = include_diversity(old_populations, T=temperature)
    print(f"  Tau = {temperature}")
    M = 0
    for p,u in zip(populations,accuracy):
        M += p*u
    print(f"\tMu score: {M}")
    print(f"\tSimple macro-averaged accuracy: {np.average(accuracy)}")
    gini_coeff = gini(np.array(populations)*N, accuracy)
    print(f"\tGini Coefficient: {gini_coeff}")
    


print("counterfactual_accuracy_spa")
accuracy = counterfactual_accuracy_spa
for temperature in [1,0.1]:
    populations = include_diversity(old_populations, T=temperature)
    print(f"  Tau = {temperature}")
    M = 0
    for p,u in zip(populations,accuracy):
        M += p*u
    print(f"\tMu score: {M}")
    print(f"\tSimple macro-averaged accuracy: {np.average(accuracy)}")
    gini_coeff = gini(np.array(populations)*N, accuracy)
    print(f"\tGini Coefficient: {gini_coeff}")
    


print("counterfactual_accuracy_linear")
accuracy = counterfactual_accuracy_linpop
for temperature in [1,0.1]:
    populations = include_diversity(old_ordered_populations, T=temperature)
    print(f"  Tau = {temperature}")
    M = 0
    for p,u in zip(populations,accuracy):
        M += p*u
    print(f"\tMu score: {M}")
    print(f"\tSimple macro-averaged accuracy: {np.average(accuracy)}")
    gini_coeff = gini(np.array(populations)*N, accuracy)
    print(f"\tGini Coefficient: {gini_coeff}")
    

print("counterfactual_accuracy_largepop")
accuracy = counterfactual_accuracy_largepop
for temperature in [1,0.1]:
    populations = include_diversity(old_ordered_populations, T=temperature)
    print(f"  Tau = {temperature}")
    M = 0
    for p,u in zip(populations,accuracy):
        M += p*u
    print(f"\tMu score: {M}")
    print(f"\tSimple macro-averaged accuracy: {np.average(accuracy)}")
    gini_coeff = gini(np.array(populations)*N, accuracy)
    print(f"\tGini Coefficient: {gini_coeff}")
    

print("counterfactual_accuracy_smallpop")
accuracy = counterfactual_accuracy_smallpop
for temperature in [1,0.1]:
    populations = include_diversity(old_ordered_populations, T=temperature)
    print(f"  Tau = {temperature}")
    M = 0
    for p,u in zip(populations,accuracy):
        M += p*u
    print(f"\tMu score: {M}")
    print(f"\tSimple macro-averaged accuracy: {np.average(accuracy)}")
    gini_coeff = gini(np.array(populations)*N, accuracy)
    print(f"\tGini Coefficient: {gini_coeff}")
"""

N = np.sum(ordered_populations)
TOTAL_LANGS = 6500
TOTAL_POPULATION = constants.TOTAL_POPULATION / 1000000
remaining_langs = TOTAL_LANGS - len(languages)
remaining_pop = TOTAL_POPULATION - N
print(remaining_langs, remaining_pop)
old_ordered_populations = [0] + [p / N for p in ordered_populations]
xs = np.cumsum(old_ordered_populations)
ys = np.linspace(0, 1, num=len(languages) + 1, endpoint=True)
print(len(xs), len(ys))
with open("curve1.tsv", "w") as op:
    for i in range(len(xs)):
        op.write(f"{xs[i]}\t{ys[i]}\n")
with open("curve2.tsv", "w") as op:
    for i in range(len(xs)):
        op.write(f"{ys[i]}\t{xs[i]}\n")

plt.plot(xs, ys)
plt.plot(ys, xs)
plt.show()
