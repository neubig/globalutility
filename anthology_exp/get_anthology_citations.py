import semanticscholar as sch
import numpy as np
import json
import time
import os, glob
import gzip


def read_all_ss(dir="sscholar", dois=None):
    doi2details = {}
    with open("filtered_sscholar.tsv", "w") as op:
        op.write("DOI\tauthors\tSSID\tTitle\tCitations\tVenue\tYear\n")
        for i in range(0, 6000):
            try:
                if i % 20 == 0:
                    print(f"{dir}/s2-corpus-{i:03d}.gz")

                with gzip.open(f"{dir}/s2-corpus-{i:03d}.gz", "rb") as f:
                    lines = f.readlines()
                data = [json.loads(l.strip()) for l in lines]
                for d in data:
                    if d["doi"] in dois:
                        doi2details[d["doi"]] = (
                            d["doi"],
                            ",".join([k["name"] for k in d["authors"]]),
                            d["id"],
                            d["title"],
                            str(len(d["inCitations"])),
                            d["venue"],
                            str(d["year"]),
                        )
                        top = "\t".join(doi2details[d["doi"]])
                        op.write(f"{top}\n")
            except:
                print(f"ERROR IN {dir}/s2-corpus-{i:03d}.gz")
                pass
    return doi2details


with open("anthology.tsv") as inp:
    lines = inp.readlines()

PID2doi = {}
PID2url = {}
alldois = set()
for l in lines:
    l = l.strip().split("\t")
    PID2doi[l[0]] = l[1]
    PID2url[l[0]] = l[2]
    alldois.add(l[1])

print(len(alldois))
doi2details = read_all_ss("sscholar", alldois)
print(len(doi2details))
