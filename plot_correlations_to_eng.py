import constants
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpl_patches
from matplotlib.cm import get_cmap
from scipy.stats import pearsonr, spearmanr
from numpy.polynomial.polynomial import polyfit

corr_func = spearmanr

plt.rcParams["font.family"] = "sans-serif"
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
all_bleus = constants.read_BLEUs()
all_populations = constants.read_mt_populations(L1only=True)


for INTEREST in "ell,fra,spa,eng,cmn,swa,swe,fin,deu,hin".split(","):

    languages = constants.get_mt_languages()
    languages.remove(INTEREST)
    try:
        languages.remove("uig")
        languages.remove("epo")
        languages.remove("nno")
    except:
        pass

    populations = [all_populations[l] for l in languages]
    NS = np.sum(populations)
    paper_num = constants.read_number_of_papers()
    internal_paper_num = constants.read_number_of_internal_papers()
    accuracy = [all_bleus[l, INTEREST] for l in languages]
    M = max(accuracy)
    utility = [(all_bleus[l, INTEREST] / M) for l in languages]
    bleus = [(all_bleus[l, INTEREST]) for l in languages]

    papers = [
        paper_num[l, INTEREST] + internal_paper_num[INTEREST, l] for l in languages
    ]
    ec_dem1 = [
        (demand1[l, INTEREST] + demand1[l, INTEREST]) / 1000.0 for l in languages
    ]
    ec_dem2 = [
        (demand2[l, INTEREST] + demand2[l, INTEREST]) / 1000.0 for l in languages
    ]

    rho1 = corr_func(populations, utility)
    print(f"rho (pop,utility) = {rho1}")
    rho2 = corr_func(ec_dem1, utility)
    print(f"rho (ec_dem1,utility) = {rho2}")
    rho3 = corr_func(ec_dem2, utility)
    print(f"rho (ec_dem2,utility) = {rho2}")
    rho4 = corr_func(papers, utility)
    print(f"rho (papers,utility) = {rho3}")

    fig, ax = plt.subplots(1, 4, figsize=(10, 2))

    ax[0].scatter(
        populations, utility, marker="o", s=10, facecolors="none", edgecolors="blue"
    )
    ax[0].set_xlabel("Population (millions)", fontsize=11)
    ax[0].set_ylabel("Per-Person Utility", fontsize=11)

    mmax = max(populations)
    for i in range(len(populations)):
        lang = languages[i]
        if papers[i] > 25 or populations[i] > 0.3 * mmax or utility[i] == 1:
            if lang in "slv,hrv".split(","):
                ax[0].annotate(
                    lang,
                    (populations[i], utility[i]),
                    textcoords="offset points",
                    ha="center",
                    fontweight="bold",
                    xytext=(0, -10),
                )
            elif lang in "ron".split(","):
                ax[0].annotate(
                    lang,
                    (populations[i], utility[i]),
                    textcoords="offset points",
                    ha="center",
                    fontweight="bold",
                    xytext=(11, -3),
                )
            elif lang in "hin".split(","):
                ax[0].annotate(
                    lang,
                    (populations[i], utility[i]),
                    textcoords="offset points",
                    ha="center",
                    fontweight="bold",
                    xytext=(11, -4),
                )
            elif lang in "deu".split(","):
                ax[0].annotate(
                    lang,
                    (populations[i], utility[i]),
                    textcoords="offset points",
                    ha="center",
                    fontweight="bold",
                    xytext=(13, -5),
                )
            elif lang in "cmn".split(","):
                ax[0].annotate(
                    lang,
                    (populations[i], utility[i]),
                    textcoords="offset points",
                    ha="center",
                    fontweight="bold",
                    xytext=(-6, 4),
                )
            else:
                ax[0].annotate(
                    lang,
                    (populations[i], utility[i]),
                    textcoords="offset points",
                    ha="center",
                    fontweight="bold",
                    xytext=(0, 4),
                )
    p3 = np.poly1d(np.polyfit(populations, utility, 3))
    x = np.linspace(0, max(populations), 1000)
    ax[0].plot(x, p3(x), "-", c="blue", alpha=0.3, linewidth=10)
    handles = [
        mpl_patches.Rectangle((0, 0), 1, 1, fc="white", ec="white", lw=0, alpha=0)
    ]
    labels = [f"ρ={rho1[0]:.2f}"]
    ax[0].legend(
        handles,
        labels,
        loc="best",
        fontsize=11,
        fancybox=True,
        framealpha=0.7,
        handlelength=0,
        handletextpad=0,
    )

    ax[1].scatter(
        ec_dem1, utility, marker="o", s=10, facecolors="none", edgecolors="blue"
    )
    ax[1].set_xlabel(f"Economic Indicators:\nImports ($1B) ", fontsize=11)
    mmax = max(ec_dem1) * 0.3
    for i in range(len(ec_dem1)):
        lang = languages[i]
        if papers[i] > 18 or ec_dem1[i] > mmax:
            if lang in "slv,hrv".split(","):
                ax[1].annotate(
                    lang,
                    (ec_dem1[i], utility[i]),
                    textcoords="offset points",
                    ha="center",
                    fontweight="bold",
                    xytext=(0, -10),
                )
            elif lang in "deu,jpn".split(","):
                ax[1].annotate(
                    lang,
                    (ec_dem1[i], utility[i]),
                    textcoords="offset points",
                    ha="center",
                    fontweight="bold",
                    xytext=(13, -5),
                )
            elif lang in "cmn".split(","):
                ax[1].annotate(
                    lang,
                    (ec_dem1[i], utility[i]),
                    textcoords="offset points",
                    ha="center",
                    fontweight="bold",
                    xytext=(-4, 4),
                )
            elif lang in "spa".split(","):
                ax[1].annotate(
                    lang,
                    (ec_dem1[i], utility[i]),
                    textcoords="offset points",
                    ha="center",
                    fontweight="bold",
                    xytext=(-4, 4),
                )
            elif lang in "ron".split(","):
                ax[1].annotate(
                    lang,
                    (ec_dem1[i], utility[i]),
                    textcoords="offset points",
                    ha="center",
                    fontweight="bold",
                    xytext=(2, 4),
                )
            elif lang in "nld".split(","):
                ax[1].annotate(
                    lang,
                    (ec_dem1[i], utility[i]),
                    textcoords="offset points",
                    ha="center",
                    fontweight="bold",
                    xytext=(-2, 2),
                )
            else:
                ax[1].annotate(
                    lang,
                    (ec_dem1[i], utility[i]),
                    textcoords="offset points",
                    ha="center",
                    fontweight="bold",
                    xytext=(0, 4),
                )
    p3 = np.poly1d(np.polyfit(ec_dem1, utility, 3))
    x = np.linspace(0, max(ec_dem1), 1000)
    ax[1].plot(x, p3(x), "-", c="blue", alpha=0.3, linewidth=10)
    handles = [
        mpl_patches.Rectangle((0, 0), 1, 1, fc="white", ec="white", lw=0, alpha=0)
    ]
    labels = [f"ρ={rho2[0]:.2f}"]
    ax[1].legend(
        handles,
        labels,
        loc="best",
        fontsize=11,
        fancybox=True,
        framealpha=0.7,
        handlelength=0,
        handletextpad=0,
    )

    ax[2].scatter(
        ec_dem2, utility, marker="o", s=10, facecolors="none", edgecolors="blue"
    )
    ax[2].set_xlabel(f"Economic Indicators:\nExports ($1B) ", fontsize=11)
    mmax = max(ec_dem2) * 0.3
    for i in range(len(ec_dem2)):
        lang = languages[i]
        if papers[i] > 25 or ec_dem2[i] > mmax:
            if lang in "slv,hrv".split(","):
                ax[2].annotate(
                    lang,
                    (ec_dem2[i], utility[i]),
                    textcoords="offset points",
                    ha="center",
                    fontweight="bold",
                    xytext=(0, -10),
                )
            elif lang in "deu,jpn".split(","):
                ax[2].annotate(
                    lang,
                    (ec_dem2[i], utility[i]),
                    textcoords="offset points",
                    ha="center",
                    fontweight="bold",
                    xytext=(13, -5),
                )
            elif lang in "cmn".split(","):
                ax[2].annotate(
                    lang,
                    (ec_dem2[i], utility[i]),
                    textcoords="offset points",
                    ha="center",
                    fontweight="bold",
                    xytext=(0, 4),
                )
            elif lang in "spa".split(","):
                ax[2].annotate(
                    lang,
                    (ec_dem2[i], utility[i]),
                    textcoords="offset points",
                    ha="center",
                    fontweight="bold",
                    xytext=(-4, 4),
                )
            elif lang in "fra".split(","):
                ax[2].annotate(
                    lang,
                    (ec_dem2[i], utility[i]),
                    textcoords="offset points",
                    ha="center",
                    fontweight="bold",
                    xytext=(0, 4),
                )
            elif lang in "ron".split(","):
                ax[2].annotate(
                    lang,
                    (ec_dem2[i], utility[i]),
                    textcoords="offset points",
                    ha="center",
                    fontweight="bold",
                    xytext=(2, 4),
                )
            elif lang in "nld".split(","):
                ax[2].annotate(
                    lang,
                    (ec_dem2[i], utility[i]),
                    textcoords="offset points",
                    ha="center",
                    fontweight="bold",
                    xytext=(-2, 2),
                )
            else:
                ax[2].annotate(
                    lang,
                    (ec_dem2[i], utility[i]),
                    textcoords="offset points",
                    ha="center",
                    fontweight="bold",
                    xytext=(0, 4),
                )
    p3 = np.poly1d(np.polyfit(ec_dem2, utility, 3))
    x = np.linspace(0, max(ec_dem2), 1000)
    ax[2].plot(x, p3(x), "-", c="blue", alpha=0.3, linewidth=10)
    handles = [
        mpl_patches.Rectangle((0, 0), 1, 1, fc="white", ec="white", lw=0, alpha=0)
    ]
    labels = [f"ρ={rho3[0]:.2f}"]
    ax[2].legend(
        handles,
        labels,
        loc="best",
        fontsize=11,
        fancybox=True,
        framealpha=0.7,
        handlelength=0,
        handletextpad=0,
    )

    ax[3].scatter(
        papers, utility, marker="o", s=10, facecolors="none", edgecolors="blue"
    )
    ax[3].set_xlabel("#Papers", fontsize=11)
    for i in range(len(accuracy)):
        lang = languages[i]
        if papers[i] > 17 or utility[i] > 0.9:
            if lang in "slv,hrv".split(","):
                ax[3].annotate(
                    lang,
                    (papers[i], utility[i]),
                    textcoords="offset points",
                    ha="center",
                    fontweight="bold",
                    xytext=(0, -10),
                )
            elif lang in "deu".split(","):
                ax[3].annotate(
                    lang,
                    (papers[i], utility[i]),
                    textcoords="offset points",
                    ha="center",
                    fontweight="bold",
                    xytext=(2, -10),
                )
            elif lang in "cmn".split(","):
                ax[3].annotate(
                    lang,
                    (papers[i], utility[i]),
                    textcoords="offset points",
                    ha="center",
                    fontweight="bold",
                    xytext=(4, 2),
                )
            elif lang != "kin":
                ax[3].annotate(
                    lang,
                    (papers[i], utility[i]),
                    textcoords="offset points",
                    ha="center",
                    fontweight="bold",
                    xytext=(0, 4),
                )

    p3 = np.poly1d(np.polyfit(papers, utility, 3))
    x = np.linspace(0, max(papers), 100)
    ax[3].plot(x, p3(x), "-", c="blue", alpha=0.3, linewidth=10)
    handles = [
        mpl_patches.Rectangle((0, 0), 1, 1, fc="white", ec="white", lw=0, alpha=0)
    ]
    labels = [f"ρ={rho4[0]:.2f}"]
    ax[3].legend(
        handles,
        labels,
        loc="best",
        fontsize=11,
        fancybox=True,
        framealpha=0.7,
        handlelength=0,
        handletextpad=0,
    )

    plt.tight_layout()
    plt.subplots_adjust(wspace=0.2)
    plt.show()

    fig.savefig(
        f"figs/to_lang/bleu_correlations_to_{INTEREST}_L1only.pdf",
        quality=100,
        format="pdf",
    )
