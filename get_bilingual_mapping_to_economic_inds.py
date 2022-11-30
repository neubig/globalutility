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
colors = cmap.colors * 200  # type: list


languages = constants.get_all_language_pairs()
languages2 = list(
    sorted(list(set([l[0] for l in languages] + [l[1] for l in languages])))
)
languages2.remove("uig")
languages2.remove("epo")

print(languages2)
demand1 = constants.read_economic_indicators(
    languages2, ind_type="Import", ind="Top 5 absolute"
)
demand2 = constants.read_economic_indicators(
    languages2, ind_type="Export", ind="Top 5 absolute"
)
all_bleus = constants.read_triangulated_BLEUs()

with open("economic_indicators_data/bilingual_indicators.tsv", "w") as op:
    op.write("L1\tL2\tBLEU\tImport (L1<-L2)\tExport(L1->L2)\tTotal\n")
    for l1 in languages2:
        for l2 in languages2:
            if l1 != l2:
                try:
                    op.write(
                        f"{l1}\t{l2}\t{all_bleus[l1,l2]}\t{demand1[l1,l2]}\t{demand2[l1,l2]}\t{demand1[l1,l2]+demand2[l1,l2]}\n"
                    )
                except:
                    pass
