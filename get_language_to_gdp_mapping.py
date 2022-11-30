import constants
import numpy as np

languages = constants.get_all_languages()
all_populations = constants.read_all_populations()
languages2 = list(languages)

try:
    languages.remove("alb")
    languages.remove("khi")
    languages.remove("may")
    languages.remove("nah")
    # languages.remove('uig')
    # languages.remove('epo')
    # languages.remove('nno')
except:
    pass


demand1 = constants.read_gdp(languages)
ec_dem1 = [demand1[l] for l in languages]
populations = [all_populations[l] for l in languages]

with open("economic_indicators_data/languages_to_gdp.tsv", "w") as op:
    op.write("ISO\tPopulation (million)\tGDP\n")
    for i, l in enumerate(languages):
        op.write(f"{l}\t{populations[i]}\t{ec_dem1[i]}\n")
