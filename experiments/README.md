# File Structure

* `populations`: contains .tsv files with language-population data and other population-relevant data

* `task_results`: contains .tsv files with the aggregated results for each NLP task.

* `economic_indicators_data`: contains files from WITS (under `wits_en_trade_summary_allcountries_allyears`) and converted to map to languages instead of countries. Important files are: 
	- `languages_to_gdp.tsv` for monolingual mapping of languages to associated GDP estimations.
	- `bilingual_indicators.tsv` for bilingual mapping of languages to associated bilingual indicators (Imports, Exports) estimations.	Also includes the triangulated BLEU scores for the language pair.

* `figs`: contains correlation figures, created with the `plot_*_correlations.py` scripts.

## Other files:
* `counterfactuals.py`: computes the counterfactual scenarios presented in the paper
* `constants.py` contains functions to read in all necessary data, which are used in other files to run the metrics estimations and produce the plots
* `economic_indicators.py`: contains function to read in economic indicators (called by `constants.py`)

## TO-DO
1. Add general metric calculation script
2. Data paths are all absolute, need to correct this
