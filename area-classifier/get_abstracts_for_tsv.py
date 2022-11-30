import argparse
import re
from sklearn.model_selection import cross_val_score
from pybtex.database.input import bibtex
import pybtex.database
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm, ensemble
import numpy as np
import sys

# Make parser object
p = argparse.ArgumentParser(
    description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
)
p.add_argument(
    "tsv_file", type=str, help="File of abstracts to classify, plain-text one per line"
)
p.add_argument(
    "output_file", type=str, help="A file where we can write out the different areas"
)
p.add_argument(
    "--anthology_file",
    help="Location of the anthology bib file",
    default="data/anthology+abstracts.bib",
)
args = p.parse_args()

# # Get info about anthology
# parser = bibtex.Parser()
# bib_data = parser.parse_file(args.anthology_file)
# for key in bib_data.entries.keys():
#   print(bib_data.entries[key].fields['title'])

url_to_abstract = {}
with open(args.anthology_file, "r") as anthology_in:
    all_lines = []
    for line in anthology_in:
        line = line.strip("\n")
        all_lines.append(line)
        if line == "}":
            entry_text = "\n".join(all_lines)
            all_lines = []
            try:
                bib_data = pybtex.database.parse_string(entry_text, "bibtex")
                for entry in bib_data.entries:
                    entry = bib_data.entries[entry]
                    if "url" in entry.fields:
                        url_to_abstract[entry.fields["url"]] = entry.fields[
                            "abstract" if "abstract" in entry.fields else "title"
                        ]
            except:
                print(entry_text)

# Get the examples
with open(args.tsv_file, "r") as tsv_in, open(args.output_file, "w") as abs_out:
    for line in tsv_in:
        cols = line.strip("\n").split("\t")
        print(url_to_abstract[cols[6]], file=abs_out)
