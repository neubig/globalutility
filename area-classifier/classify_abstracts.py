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
p = argparse.ArgumentParser(description=__doc__,
                            formatter_class=argparse.RawDescriptionHelpFormatter)
p.add_argument("abstract_file", type=str, help="File of abstracts to classify, plain-text one per line")
p.add_argument("output_file", type=str, help="A file where we can write out the different areas")
p.add_argument("--anthology_file",
               help="Location of the anthology bib file",
               default="data/anthology+abstracts.bib")
p.add_argument("--venues_file",
               help="Location of the venues tsv file",
               default="data/acl-areas.tsv")
args = p.parse_args()

# Get info about venues
venue_to_area_map = {}
area_names = []
with open(args.venues_file, 'r') as venues_in:
  next(venues_in) #remove the header
  for line in venues_in:
    cols = line.strip('\n').split('\t')
    # print(cols)
    if len(cols[0]):
      area_names.append(cols[0])
    venue_to_area_map[cols[2]] = len(area_names)-1
venue_regex = re.compile('('+'|'.join(venue_to_area_map.keys())+')')

# # Get info about anthology
# parser = bibtex.Parser()
# bib_data = parser.parse_file(args.anthology_file)
# for key in bib_data.entries.keys():
#   print(bib_data.entries[key].fields['title'])

anthology_x = []
anthology_y = []
with open(args.anthology_file, 'r') as anthology_in:
  all_lines = []
  for line in anthology_in:
    line = line.strip('\n')
    all_lines.append(line)
    if line == '}':
      entry_text = '\n'.join(all_lines)
      all_lines = []
      m = re.search(venue_regex, entry_text)
      if m:
        bib_data = pybtex.database.parse_string(entry_text, 'bibtex')
        label_y = venue_to_area_map[m.group(1)]
        for entry in bib_data.entries:
          entry = bib_data.entries[entry]
          anthology_x.append(entry.fields['abstract' if 'abstract' in entry.fields else 'title'])
          anthology_y.append(label_y)

# Get the examples
example_x = []
example_y = []
with open(args.abstract_file, 'r') as abstract_in:
  example_x = [x.strip() for x in abstract_in]

# Train the BOW classifier
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(anthology_x + example_x)
anthology_feat = X[:len(anthology_x)]
example_feat = X[len(anthology_x):]
print('cross-validating...', file=sys.stderr)
coefs = [1e-4, 2e-4, 5e-4, 1e-3, 2e-3, 5e-3, 1e-2, 2e-2, 5e-2, 1e-1, 2e-1, 5e-1]
coef_scores = []
for c in coefs:
  clf = svm.LinearSVC(C=c)
  scores = cross_val_score(clf, anthology_feat, anthology_y, cv=5)
  avg_score = sum(scores)/len(scores)
  coef_scores.append(avg_score)
  print(f'{c}: {avg_score}', file=sys.stderr)
my_coef = coefs[np.argmax(coef_scores)]
print(f'classifying with coefficient {my_coef}', file=sys.stderr)
clf = svm.LinearSVC(C=my_coef)
trained_clf = clf.fit(anthology_feat, anthology_y)

# Classify the examples
example_yhat = trained_clf.predict(example_feat)
with open(args.output_file, 'w') as output_out:
  for aid in example_yhat:
    print(area_names[aid], file=output_out)