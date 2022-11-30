import semanticscholar as sch
import numpy as np
import json
import time
import os, glob
import gzip
import csv
from nltk import word_tokenize


def read_sscholar(f="filtered_sscholar.tsv"):
    with open(f) as inp:
        lines = inp.readlines()
    doi2details = {}
    for l in lines[1:]:
        l = l.split("\t")
        # print(l)
        doi = l[0]
        authors = l[1]
        SSID = l[2]
        title = l[3]
        citations = l[4]
        venue = l[5]
        year = l[6].strip()
        doi2details[doi] = (authors, SSID, title, citations, venue, year)
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

print(f"Number of Anthology DOIS: {len(alldois)}")
doi2details = read_sscholar()
print(f"Number of DOIS found in Semantic Scholar: {len(doi2details)}")

all_languages = {}
with open("languages_and_dialects_geo.csv") as inp:
    csvreader = csv.reader(inp, delimiter=",", quotechar='"')
    firstline = True
    languages_to_ignore = "Laura,Fang,Mono,Ma,Maria,Sam,Bench,Zhuang,Male,Nara,So,Hu,Kim,Label,The,To,Yong,The,To,Adele,Are,Foma,Kaur,Bau,Kato,Dek,Naman,Dom,As,The,To,As,Dan,E,The,To,U,Even,En,Chung,Dong,Shi,Tai,Thompson,Gao,Ir,Pan,Ali,Rao,Han,Doe,Titan,Ha,Sa,Tu,Lau,Siri,Wan,She,Dai,Ding,Kang,Ge,Koch,Che,Mann,Zou,Pei,Yao,Lou,Sydney,Ju,Sha,Day,Miwa,Bai,Ko,Ga,Pal,Pe,Gun,Hung,Con,Cun,Serrano,Sui,Bu,Mehri,Od,Haji,Gal,Gey,Lui,Ho,Furu,Ak,Kao,Aro,Gen,Moro,Notre,Ido,Ron,Were,Bai,Sahu,Dem,Melo,Rama,Hunde,Dii,Yala,Sauri".split(
        ","
    )
    for line in csvreader:
        if firstline:
            firstline = False
            continue
        glottocode = line[0]
        iso = line[2]
        name = line[1]
        level = line[3]
        if level == "language" and iso and name not in languages_to_ignore:
            all_languages[name] = (iso, glottocode)

with open("filtered_ethnologue.tsv") as inp:
    csvreader = csv.reader(inp, delimiter="\t", quotechar='"')
    firstline = True
    languages_to_ignore = "Laura,Fang,Mono,Ma,Maria,Sam,Bench,Zhuang,Male,Nara,So,Hu,Kim,Label,The,To,Yong,The,To,Adele,Are,Foma,Kaur,Bau,Kato,Dek,Naman,Dom,As,The,To,As,Dan,E,The,To,U,Even,En,Chung,Dong,Shi,Tai,Thompson,Gao,Ir,Pan,Ali,Rao,Han,Doe,Titan,Ha,Sa,Tu,Lau,Siri,Wan,She,Dai,Ding,Kang,Ge,Koch,Che,Mann,Zou,Pei,Yao,Lou,Sydney,Ju,Sha,Day,Miwa,Bai,Ko,Ga,Pal,Pe,Gun,Hung,Con,Cun,Serrano,Sui,Bu,Mehri,Od,Haji,Gal,Gey,Lui,Ho,Furu,Ak,Kao,Aro,Gen,Moro,Notre,Ido,Ron,Were,Bai,Sahu,Dem,Melo,Rama,Hunde,Dii,Yala,Sauri".split(
        ","
    )
    for line in csvreader:
        if firstline:
            firstline = False
            continue
        glottocode = ""
        iso = line[0].strip()
        name = line[2].strip()
        # level = line[3]
        if iso and name not in languages_to_ignore:
            if name not in all_languages:
                all_languages[name] = (iso, glottocode)

# Add macrolanguages
macrolist = {}
with open("macrolanguages.tsv") as inp:
    lines = inp.readlines()
for l in lines:
    l = l.strip().split("\t")
    iso = l[0]
    name = l[1]
    iso2 = l[2]
    name2 = l[3]
    all_languages[name] = (iso, "dummy_glottocode")
    if name2 in all_languages:
        macrolist[name2] = name


def search_languages(f):
    langlist = []
    with open(f) as inp:
        text = inp.read()
    i = text.find("Abstract")
    j = text.find("Acknowledgment")
    if j == -1:
        j = text.find("References")
    if i != -1 and j != -1:
        text = text[i:j]
    for l in all_languages:
        ADD_MACRO = False
        if l in macrolist:
            ADD_MACRO = True
        if " " + l + " " in text:
            print(l, all_languages[l][0])
            langlist.append(all_languages[l][0])
            if ADD_MACRO:
                langlist.append(all_languages[macrolist[l]][0])
        elif " " + l + "," in text:
            print(l, all_languages[l][0])
            langlist.append(all_languages[l][0])
            if ADD_MACRO:
                langlist.append(all_languages[macrolist[l]][0])
        elif " " + l + "." in text:
            print(l, all_languages[l][0])
            langlist.append(all_languages[l][0])
            if ADD_MACRO:
                langlist.append(all_languages[macrolist[l]][0])
    return langlist


print(f"Number of languages: {len(all_languages)}")

with open("anthology_citation_language_info.tsv", "w") as op:
    confs = os.listdir("anthology/text")
    # confs = ['acl2019']
    for c in confs:
        print(c)

        files = os.listdir(f"anthology/text/{c}")
        if "naacl" in c:
            conf_id = "N"
        elif "emnlp" in c:
            conf_id = "D"
        elif "eacl" in c:
            conf_id = "E"
        elif "aacl" in c:
            conf_id = "A"
        elif "acl" in c:
            conf_id = "P"
        year = c[-4:]
        year2 = c[-2:]
        for f in files:
            # Format: 2012.emnlp-main.1046.txt
            print(f)
            f2 = f.strip().split(".")
            ID = f2[-2]
            PID = f"{conf_id}{year2}-{ID}"
            if (conf_id == "D" or conf_id == "P") and year == "2020":
                doi = f"10.18653/v1/{'.'.join(f2[:3])}"
                print(doi)
                PID2doi[PID] = doi
                PID2url[PID] = f"https://www.aclweb.org/anthology/{'.'.join(f2[:3])}"

            if PID in PID2doi:
                doi = PID2doi[PID]
                print(f"DOI: {doi}")
                url = PID2url[PID]
                print(f"DOI in doi2details: {doi in doi2details}")
                if doi in doi2details:
                    # print("Got in doi2details")
                    try:
                        citations = doi2details[doi][3]
                    except:
                        citations = -1
                        pass
                    # try:
                    # 	citation_velocity = paper['citationVelocity']
                    # except:
                    # 	citation_velocity = -1
                    # 	pass
                    # title = paper['title'].strip()
                    title = doi2details[doi][2]
                    authors = doi2details[doi][0]
                    venue = doi2details[doi][4]
                    year = doi2details[doi][5]
                    paperID = doi2details[doi][1]
                    langs = search_languages(f"anthology/text/{c}/{f}")
                    # lang_iso_codes = ','.join([all_languages[lang][0] for lang in langs])
                    # op.write(f"{paperID}\t{venue}\t{year}\t{title}\t{authors}\t{citations}\t{url}\t{doi}\t{','.join(langs)}\t{lang_iso_codes}\n")
                    op.write(
                        f"{paperID}\t{venue}\t{year}\t{title}\t{authors}\t{citations}\t{url}\t{doi}\t{','.join(langs)}\n"
                    )
