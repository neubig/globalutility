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

print(len(languages))
print(len(populations))


def include_diversity(l, T=1):
    acc_arr = np.array(l)
    acc_arr = [f**T for f in acc_arr]
    N = sum(acc_arr)
    acc_arr = [f / N for f in acc_arr]
    return list(acc_arr)


N = np.sum(populations)
old_populations = [p / N for p in populations]

NUM_LANGUAGES = len(languages)
# Sort demand from largest to smallest
inds = np.flip(np.argsort(old_populations))
old_populations = [old_populations[i] for i in inds]

# pre-compute adjusted demand
populations1 = np.array(include_diversity(old_populations, T=1))
populations01 = np.array(include_diversity(old_populations, T=0.1))
Npopulations1 = np.array(populations1) * N
Npopulations01 = np.array(populations01) * N


for counterfactual_accuracy in [1, 0.9, 0.8, 0.7]:
    cum1 = np.cumsum(populations1 * counterfactual_accuracy)
    cum01 = np.cumsum(populations01 * counterfactual_accuracy)
    print(cum1[:3])
    print("***")
    print(cum01[:3])
    plt.plot(cum1, cum01)

    with open(f"figs/counterfactual_curve_{counterfactual_accuracy}.tsv", "w") as op:
        prev = ""
        for x, y in zip(cum1, cum01):
            towrite = f"{x:.2f} & {y:.2f} \\\\ \n"
            if towrite != prev:
                prev = towrite
                op.write(towrite)
plt.show()
