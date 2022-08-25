Below are the steps for recreating our analysis.

## 1. Get the anthology

Follow the instructions in the `anthology` directory to download PDFs and convert them to txt.

## 2. Convert the anthology bib file into a more easy-to-use format

Use script `convert_anthology_to_csv.py`, which reads in the anthology .bib file (you can get that from [here](https://aclanthology.org/)) into a .tsv with the fields we care about (we need: title, url, DOI, ID).

This will produce an `anthology.tsv` file.

# 3. Get citation information for a list of anthology papers

First, download the S2 corpus from semantic scholar [paper](https://aclanthology.org/2020.acl-main.447/) [data](https://allenai.org/data/s2orc), that contains citation information. Unpack it into the `sscholar` directory. *Note: requires 180GB on disk*

The `get_anthology_citations.py` first reads in the `anthology.tsv` file we created above, and then searches through the 6000 files of the S2 corpus for their entries.
The output is the file `filtered_sscholar.tsv` which has the following columns: `DOI` `authors` `SSID` `Title` `Citations` `Venue` `Year`.

# 4. Get language statistics from the papers' content

Use the `get_anthology_languages.py`. This script first reads in the `anthology.tsv` file and the `filtered_sscholar.tsv` files.

Then it reads in language information files:
- the list of languages from `languages_and_dialects_geo.csv` to get information on language names, ISO codes, and Glottocodes. *Note: there's a hard-coded list of language names to ignore because they match very common English/Chinese word/names, e.g."Laura,Fang,Mono,Ma,..."*
- the language information from `filtered_ethnologue.tsv`
- and the macrolanguage information from `macrolanguages.tsv`

Then it goes through the txt files of the papers (assumed to be under `anthology/text`); for each paper it reconstructs its DOI; if it was found in Semantic Scholar it gets its citation information; it then searches the text for language names/codes by calling function `search_languages()`;  and produces the final output file (e.g. `anthology_citation_language_info.tsv`) which contains all the information needed for our analyses.

The script writes out a file `anthology_citation_language_info.tsv`



# Additional analysis
Script `get_anthology_language_statistics.py` reads in the citation and language info file (`anthology_citation_language_info.tsv`) and produces the counts of how many papers mention N number of languages in their content.