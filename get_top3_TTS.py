import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle
from matplotlib.cm import get_cmap
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


def METRIC(populations, accuracy):
    # normalized populations (sum to 1)
    # normalized accuracy (max is 1)
    mu = 0
    area_covered = []
    area_missing = []
    for p, a in zip(populations, accuracy):
        mu += p * a
        area_covered.append(p * a)
        area_missing.append(p * (1 - a))
    return mu, area_covered, area_missing


task = "tts"
total_lang = -1


TOTAL_POPULATION = constants.TOTAL_POPULATION / 1000000

all_populations = constants.read_synthesis_populations()
languages = constants.get_wilderness_languages()
languageso = constants.get_wilderness_languages()
pop_denom = constants.TOTAL_POPULATION / 1000000
all_bleus = constants.read_wilderness()
# languageso.append('eng')
languages.remove("alb")
languages.remove("khi")
languages.remove("may")
languages.remove("nah")
languageso.remove("alb")
languageso.remove("khi")
languageso.remove("may")
languageso.remove("nah")

# all_bleus['eng'] = 1


populationso = [all_populations[l] for l in languages]
sumpop = np.sum(populationso)

accuracyo = [all_bleus[l] for l in languages]
# Needed because lower is better
max_accuracy = max(accuracyo)
min_accuracy = min(accuracyo)

spread = max_accuracy - min_accuracy
print(min_accuracy, max_accuracy, spread)
accuracyo = [(max_accuracy - a) / spread for a in accuracyo]


if total_lang == -1:
    TOTAL_LANGS = len(languages)
else:
    TOTAL_LANGS = 6500


def include_diversity(l, T=1):
    acc_arr = np.array(l)
    acc_arr = [f**T for f in acc_arr]
    N = sum(acc_arr)
    acc_arr = [f / N for f in acc_arr]
    return list(acc_arr)


langs_to_show = set()

temperatures = list(np.flip(np.arange(1, 11) / 10)) + [0.01]
# temperatures = [1]

for temperature in temperatures:
    remaining = TOTAL_LANGS - len(languages)
    print(remaining)
    accuracy = accuracyo + [0] * remaining
    languages = languageso + ["rest"] * remaining
    if remaining:
        tosplit = (TOTAL_POPULATION - sum(populationso)) / remaining
        populations = populationso + [tosplit] * remaining
    else:
        populations = list(populationso)

    populations = include_diversity(populations, T=temperature)
    print(len(populations), sum(populations))

    inds = np.flip(np.argsort(accuracy))
    populations = [populations[i] for i in inds]
    accuracies = [accuracy[i] for i in inds]
    languages = [languages[i] for i in inds]

    N = np.sum(populations)
    old_populations = [p / N for p in populations]

    populations = include_diversity(old_populations, T=temperature)
    gini_coeff = gini(np.array(populations) * N, accuracies)

    # normalize accuracy
    M = max(accuracies)
    accuracies = [a / M for a in accuracies]

    MU, area_covered, area_missing = METRIC(populations, accuracies)

    # print(f"Total area covered: M={sum(area_covered)}")
    # print(f"Total area missing: RoI={sum(area_missing)}")

    """
    inds = np.flip(np.argsort(area_covered))
    print(f"Top 10 Covered with tau = {temperature}")
    for i in inds[:10]:
        print(f"{i}\t{languages[i]}\t{area_covered[i]}\t{area_missing[i]}")
    """

    print(f"Mu Score: {MU}")

    inds = np.flip(np.argsort(area_missing))
    print(f"Top 3 Missing with tau = {temperature}")
    for i in inds[:3]:
        print(f"\t{i}\t{languages[i]}\t{area_missing[i]}")
