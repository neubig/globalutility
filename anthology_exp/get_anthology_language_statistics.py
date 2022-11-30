from collections import defaultdict
import numpy as np

with open("anthology_citation_language_info.tsv") as inp:
    lines = inp.readlines()

max_lang = 0
paper_with_max = ""
lang_count = defaultdict(lambda: 0)
paper_lcount = defaultdict(lambda: 0)
for l in lines:
    l = l.split("\t")
    # {paperID}\t{venue}\t{year}\t{title}\t{authors}\t{citations}\t{url}\t{doi}\t{','.join(langs)}
    doi = l[7]
    venue = l[1]
    year = l[2]
    title = l[3]
    num_cit = l[5]
    langs = l[8]
    if langs.strip():
        langs = langs.strip().split(",")
        paper_lcount[len(langs)] += 1
        if len(langs) > max_lang:
            max_lang = len(langs)
            paper_with_max = (l, max_lang)
        if len(langs) > 30:
            print("Paper with high: ", l, len(langs))
        for lang in langs:
            lang_count[lang] += 1
    else:
        paper_lcount[0] += 1


langs = []
counts = []
for k in lang_count:
    langs.append(k)
    counts.append(lang_count[k])

inds = np.argsort(counts)
for i in inds[:20]:
    print(f"{langs[i]},{counts[i]}")
print("****************************************")
for i in inds[-40:]:
    print(f"{langs[i]},{counts[i]}")

print(f"Paper with max: {paper_with_max[0]}, {paper_with_max[1]}")

print("Number of papers with languages")
for i in range(83):
    if i in paper_lcount:
        print(i, paper_lcount[i])
