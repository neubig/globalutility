import numpy as np
import constants
import copy

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

def include_diversity(l, T=1):
    acc_arr = np.array(l)
    acc_arr = [f**T for f in acc_arr]
    N = sum(acc_arr)
    acc_arr = [f/N for f in acc_arr]
    return list(acc_arr)



TOTAL_POPULATION = constants.TOTAL_POPULATION/1000000
all_populations = constants.read_sig_populations()
languages1 = constants.get_sig_languages()
languages2 = list(languages1)
languageso = list(languages1)
pop_denom = constants.TOTAL_POPULATION /1000000


prev_all_bleus = {}
print(f"year\tx (tau=1)\ty (tau->0)")
for year in range(2014, 2022):
    all_bleus = constants.read_sig(year=str(year)[-2:])
    if prev_all_bleus:
        for key in prev_all_bleus:
            if key not in all_bleus:
                all_bleus[key] = prev_all_bleus[key]
            elif prev_all_bleus[key] > all_bleus[key]:
                all_bleus[key] = prev_all_bleus[key]
    prev_all_bleus = copy.deepcopy(all_bleus)

    languages1 = constants.get_sig_languages()
    languages2 = list(languages1)
    languageso = list(languages1)

    #populationso = [all_populations[l] for l in languages2 if l !='eng' ]
    populationso = [all_populations[l] for l in languages2]
    accuracyo = [all_bleus[l1] for l1 in languages2]
    languages = list(languageso)
    

    #print(f"Year: {year}")
    #print(f"Pairs: {len(accuracyo)}")
    langs_to_show = set()

    TOTAL_LANGS = 6500
    answers = []
    for temperature in [1,0.01]:
        if temperature == 1:
            remaining = 1
        else:
            remaining = TOTAL_LANGS - len(languages)    
        accuracy = accuracyo + [0]*remaining
        languages = languageso + ['rest']*remaining
        if temperature == 1:
            tosplit = (TOTAL_POPULATION - sum(populationso))
            populations = populationso + [tosplit]
        else:
            populations = [1 for l in languages]

        
        inds = np.flip(np.argsort(accuracy))
        N = np.sum(populations)
        populations = [populations[i]/N for i in inds]
        accuracy = [accuracy[i]/100 for i in inds]
        languages = [languages[i] for i in inds]
        
        N = np.sum(populations)
        old_populations = [p/N for p in populations]

        populations = include_diversity(old_populations, T=temperature)
        gini_coeff = gini(np.array(populations)*N, accuracy)

        M_score = np.sum(np.array(populations)*np.array(accuracy))
        #print(f"temperature {temperature}: {M_score} ({len(languageso)} languages)")
        answers.append(M_score)

    print(f"{year}\t{answers[0]}\t{answers[1]}")

