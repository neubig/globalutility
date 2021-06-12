from collections import defaultdict
import economic_indicators
import os

# As of 2020
TOTAL_POPULATION = 7900000000.0
TOTAL_ENG_POPULATION = 510000000.0

population_file = "/Users/antonios/desktop/research/PNAS_Fairness/globalutility/experiments/populations/mt_populations_with_noneng.tsv"
#all_population_file = "/Users/antonios/desktop/research/PNAS_Fairness/globalutility/experiments/populations/populations.tsv"

all_population_file ="/Users/antonios/desktop/research/PNAS_Fairness/globalutility/experiments/populations/ethnologue_all_populations.tsv" 
mt_population_file = "/Users/antonios/desktop/research/PNAS_Fairness/globalutility/experiments/populations/ethnologue_mt_populations.tsv"
mtL1_population_file = "/Users/antonios/desktop/research/PNAS_Fairness/globalutility/experiments/populations/ethnologue_mt_L1_populations.tsv"
dep_population_file = "/Users/antonios/desktop/research/PNAS_Fairness/globalutility/experiments/populations/ethnologue_dep_populations.tsv"
depL1_population_file = "/Users/antonios/desktop/research/PNAS_Fairness/globalutility/experiments/populations/ethnologue_dep_L1_populations.tsv"
xnli_population_file = "/Users/antonios/desktop/research/PNAS_Fairness/globalutility/experiments/populations/ethnologue_xnli_populations.tsv"
xnliL1_population_file = "/Users/antonios/desktop/research/PNAS_Fairness/globalutility/experiments/populations/ethnologue_xnli_L1_populations.tsv"
qa_population_file = "/Users/antonios/desktop/research/PNAS_Fairness/globalutility/experiments/populations/ethnologue_qa_populations.tsv"
synthesis_population_file = "/Users/antonios/desktop/research/PNAS_Fairness/globalutility/experiments/populations/ethnologue_synthesis_populations.tsv"
sig_population_file = "/Users/antonios/desktop/research/PNAS_Fairness/globalutility/experiments/populations/ethnologue_sig_populations.tsv"
sig_isolating_population_file = "/Users/antonios/desktop/research/PNAS_Fairness/globalutility/experiments/populations/ethnologue_isolating_populations.tsv"
sigL1_population_file = "/Users/antonios/desktop/research/PNAS_Fairness/globalutility/experiments/populations/ethnologue_sig_L1_populations.tsv"
index_file = "/Users/antonios/desktop/research/PNAS_Fairness/globalutility/experiments/task_results/MT_index.tsv"
flores_index_file = "/Users/antonios/desktop/research/PNAS_Fairness/globalutility/experiments/task_results/flores_index.tsv"
triangulation_file = "/Users/antonios/desktop/research/PNAS_Fairness/globalutility/experiments/task_results/triangulated_BLEUS.tsv"
xnli_file = "/Users/antonios/desktop/research/PNAS_Fairness/globalutility/experiments/task_results/XNLI.tsv"
qa_file = "/Users/antonios/desktop/research/PNAS_Fairness/globalutility/experiments/task_results/QA.tsv"
dep_file = "/Users/antonios/desktop/research/PNAS_Fairness/globalutility/experiments/task_results/DEP.tsv"
sig_file = "/Users/antonios/desktop/research/PNAS_Fairness/globalutility/experiments/task_results/SIGMORPHON.tsv"
sig_isolating_file = "/Users/antonios/desktop/research/PNAS_Fairness/globalutility/experiments/task_results/SIGMORPHON_isolating.tsv"
sig20_file = "/Users/antonios/desktop/research/PNAS_Fairness/globalutility/experiments/task_results/SIGMORPHON2020.tsv"
sig19_file = "/Users/antonios/desktop/research/PNAS_Fairness/globalutility/experiments/task_results/SIGMORPHON2019.tsv"
sig18_file = "/Users/antonios/desktop/research/PNAS_Fairness/globalutility/experiments/task_results/SIGMORPHON2018.tsv"
sig17_file = "/Users/antonios/desktop/research/PNAS_Fairness/globalutility/experiments/task_results/SIGMORPHON2017.tsv"
sig16_file = "/Users/antonios/desktop/research/PNAS_Fairness/globalutility/experiments/task_results/SIGMORPHON2016.tsv"
wilderness_file = "/Users/antonios/desktop/research/PNAS_Fairness/globalutility/experiments/task_results/wilderness.tsv"
wilderness_countries_file = "/Users/antonios/desktop/research/PNAS_Fairness/globalutility/experiments/populations/wilderness_iso_country.tsv"
literacy_file = "/Users/antonios/desktop/research/PNAS_Fairness/globalutility/experiments/populations/literacy_data.csv"


def read_populations(L1only=False):
	# Reads the population file and returns a dictionary
	with open(population_file, 'r') as inp:
		lines = inp.readlines()

	d = {}
	for l in lines[1:]:
		if l.strip():
			l = l.strip().split('\t')
			d[l[0]] = float(l[2])/1000000
	return d

def read_mt_populations(L1only=False):
	# Reads the population file and returns a dictionary
	if L1only:	
		with open(mtL1_population_file, 'r') as inp:
			lines = inp.readlines()
	else:
		with open(mt_population_file, 'r') as inp:
			lines = inp.readlines()

	d = {}
	for l in lines:
		if l.strip():
			l = l.strip().split('\t')
			d[l[0]] = float(l[1])/1000000
	return d


def read_dep_populations(L1only=False):
	# Reads the population file and returns a dictionary
	if L1only:	
		with open(depL1_population_file, 'r') as inp:
			lines = inp.readlines()
	else:
		with open(dep_population_file, 'r') as inp:
			lines = inp.readlines()

	d = {}
	for l in lines:
		if l.strip():
			l = l.strip().split('\t')
			d[l[0]] = float(l[1])/1000000
	return d

def read_xnli_populations(L1only=False):
	# Reads the population file and returns a dictionary
	if L1only:	
		with open(xnliL1_population_file, 'r') as inp:
			lines = inp.readlines()
	else:
		with open(xnli_population_file, 'r') as inp:
			lines = inp.readlines()

	d = {}
	for l in lines:
		if l.strip():
			l = l.strip().split('\t')
			d[l[0]] = float(l[1])/1000000
	return d

def read_qa_populations(L1only=False):
	# Reads the population file and returns a dictionary
	with open(qa_population_file, 'r') as inp:
		lines = inp.readlines()

	d = {}
	for l in lines:
		if l.strip():
			l = l.strip().split('\t')
			d[l[0]] = float(l[1])/1000000
	return d

def read_synthesis_populations():
	# Reads the population file and returns a dictionary
	with open(synthesis_population_file, 'r') as inp:
		lines = inp.readlines()

	d = {}
	for l in lines:
		if l.strip():
			l = l.strip().split('\t')
			d[l[0]] = float(l[1])/1000000
	return d

def read_sig_populations(L1only=False, include_isolating=True):
	# Reads the population file and returns a dictionary
	if L1only:	
		with open(sigL1_population_file, 'r') as inp:
			lines = inp.readlines()
	else:
		with open(sig_population_file, 'r') as inp:
			lines = inp.readlines()
	if include_isolating:
		with open(sig_isolating_population_file) as inp:
			lines += inp.readlines()

	d = {}
	for l in lines:
		if l.strip():
			l = l.strip().split('\t')
			d[l[0]] = float(l[1])/1000000
	return d

def read_noneng_populations():
	# Reads the population file and returns a dictionary	
	with open(population_file, 'r') as inp:
		lines = inp.readlines()
	disc = {}
	for l in lines[1:]:
		if l.strip():
			l = l.strip().split('\t')
			disc[l[0]] = float(l[5])

	# Reads the population file and returns a dictionary
	with open(mt_population_file, 'r') as inp:
		lines = inp.readlines()
	d = read_mt_populations()
	for l in d:
		if l in disc:
			d[l] = (1-disc[l])*d[l]
	return d

def read_all_populations():
	# Synthesis
	with open(synthesis_population_file, 'r') as inp:
		lines = inp.readlines()

	d = {}
	for l in lines:
		if l.strip():
			l = l.strip().split('\t')
			d[l[0]] = float(l[1])/1000000

	# SIG
	with open(sigL1_population_file, 'r') as inp:
		lines = inp.readlines()
	for l in lines:
		if l.strip():
			l = l.strip().split('\t')
			if l[0] not in d:
				d[l[0]] = float(l[1])/1000000

	# Dep
	with open(depL1_population_file, 'r') as inp:
		lines = inp.readlines()
	for l in lines:
		if l.strip():
			l = l.strip().split('\t')
			if l[0] not in d:
				d[l[0]] = float(l[1])/1000000

	# XNLI
	with open(xnliL1_population_file, 'r') as inp:
		lines = inp.readlines()
	for l in lines:
		if l.strip():
			l = l.strip().split('\t')
			if l[0] not in d:
				d[l[0]] = float(l[1])/1000000

	# MT
	with open(mtL1_population_file, 'r') as inp:
		lines = inp.readlines()
	for l in lines:
		if l.strip():
			l = l.strip().split('\t')
			if l[0] not in d:
				d[l[0]] = float(l[1])/1000000

	# MT with non-eng file
	with open(population_file, 'r') as inp:
		lines = inp.readlines()
	for l in lines[1:]:
		if l.strip():
			l = l.strip().split('\t')
			if l[0] not in d:
				d[l[0]] = float(l[2])/1000000

	return d




def read_gdp(languages):
	return economic_indicators.read_nominal_gdp(languages)

def read_economic_indicators(languages, ind_type="Import", ind="Top 5 absolute"):
	print(f"Came in here! with languages {languages}")
	if languages:
		if not isinstance(languages, set):
			if isinstance(languages[0], tuple):
				languages2 = list(sorted(list(set ( [l[0] for l in languages] + [l[1] for l in languages]))))
				if 'absolute' in ind:
					return economic_indicators.read_absolute_economic_indicators(languages2, ind_type, ind)
				else:
					return economic_indicators.read_economic_indicators(languages2, ind_type, ind)
			else:
				languages2 = set(languages)
				languages2.add('eng')
				languages2 = list(sorted(list(languages2)))
				if 'absolute' in ind:
					return economic_indicators.read_absolute_economic_indicators(languages2, ind_type, ind)
				else:
					return economic_indicators.read_economic_indicators(languages2, ind_type, ind)

		else:
			languages2 = set(languages)
			languages2.add('eng')
			languages2 = list(sorted(list(languages2)))
			if 'absolute' in ind:
				return economic_indicators.read_absolute_economic_indicators(languages2, ind_type, ind)
			else:
				return economic_indicators.read_economic_indicators(languages2, ind_type, ind)
	else:
		if languages:
			l2 = set(languages).add('eng')
		else:
			l2 = set()
			l2.add('eng')
		languages2 = list(sorted(list(l2)))
		if 'absolute' in ind:
			return economic_indicators.read_absolute_economic_indicators(languages2, ind_type, ind)
		else:
			return economic_indicators.read_economic_indicators(languages2, ind_type, ind)
	#raise NotImplementedError("Economic Indicators demand not implemented")

def read_social_media_stats():
	raise NotImplementedError("Social Media demand not implemented")

def read_usage_stats():
	raise NotImplementedError("Usage demand not implemented")


def get_languages_to_Eng(domains=None):
	with open(index_file, 'r') as inp:
		lines = inp.readlines()
	with open(flores_index_file, 'r') as inp:
		lines += inp.readlines()[1:]

	languages = set()
	for l in lines[1:]:
		if l.strip()[0] != '#':
			l = l.strip().split('\t')
			if l[1] == 'eng' and (l[0] != 'nno'):
				if (domains is None) or any([w in domains for w in l[7].strip().split(',')]):
					languages.add(l[0])
	return sorted(list(languages))

def get_xnli_languages():
	with open(xnli_file, 'r') as inp:
		lines = inp.readlines()

	languages = set()
	for l in lines[1:]:
		l = l.strip().split('\t')
		languages.add(l[0])
	return sorted(list(languages))

def get_qa_languages():
	with open(qa_file, 'r') as inp:
		lines = inp.readlines()

	languages = set()
	for l in lines[1:]:
		l = l.strip().split('\t')
		languages.add(l[0])
	return sorted(list(languages))

def get_dep_languages():
	with open(dep_file, 'r') as inp:
		lines = inp.readlines()

	languages = set()
	for l in lines[1:]:
		l = l.strip().split('\t')
		languages.add(l[0])
	return sorted(list(languages))

def get_sig_languages(include_isolating=True):
	with open(sig_file, 'r') as inp:
		lines = inp.readlines()
	with open(sig16_file , 'r') as inp:
		lines2 = inp.readlines()
	with open(sig17_file , 'r') as inp:
		lines2 += inp.readlines()
	with open(sig18_file , 'r') as inp:
		lines2 += inp.readlines()
	with open(sig19_file , 'r') as inp:
		lines2 += inp.readlines()
	if include_isolating:
		with open(sig_isolating_file , 'r') as inp:
			lines2 += inp.readlines()

	languages = set()
	for l in lines[1:]+lines2:
		l = l.strip().split('\t')
		languages.add(l[0])
	return sorted(list(languages))

def get_all_languages():
	# SIG
	with open(sig_file, 'r') as inp:
		lines = inp.readlines()
	with open(sig16_file , 'r') as inp:
		lines2 = inp.readlines()
	with open(sig17_file , 'r') as inp:
		lines2 += inp.readlines()
	with open(sig18_file , 'r') as inp:
		lines2 += inp.readlines()
	with open(sig19_file , 'r') as inp:
		lines2 += inp.readlines()
	with open(sig_isolating_file , 'r') as inp:
		lines2 += inp.readlines()

	languages = set()
	for l in lines[1:]+lines2:
		l = l.strip().split('\t')
		languages.add(l[0])

	# DepParse
	with open(dep_file, 'r') as inp:
		lines = inp.readlines()
	for l in lines[1:]:
		l = l.strip().split('\t')
		languages.add(l[0])

	# XNLI
	with open(xnli_file, 'r') as inp:
		lines = inp.readlines()
	for l in lines[1:]:
		l = l.strip().split('\t')
		languages.add(l[0])

	# QA
	with open(qa_file, 'r') as inp:
		lines = inp.readlines()
	for l in lines[1:]:
		l = l.strip().split('\t')
		languages.add(l[0])

	# MT2Eng
	with open(index_file, 'r') as inp:
		lines = inp.readlines()
	with open(flores_index_file, 'r') as inp:
		lines += inp.readlines()[1:]
	for l in lines[1:]:
		if l.strip()[0] != '#':
			l = l.strip().split('\t')
			if l[1] == 'eng' and (l[0] != 'nno'):
				languages.add(l[0])

	# MTfrom Eng
	with open(index_file, 'r') as inp:
		lines = inp.readlines()
	with open(flores_index_file, 'r') as inp:
		lines += inp.readlines()[1:]
	for l in lines[1:]:
		if l.strip()[0] != '#':
			l = l.strip().split('\t')
			if l[0] == 'eng':
				languages.add(l[1])

	# Wilderness
	with open(wilderness_file, 'r') as inp:
		lines = inp.readlines()
	for l in lines[1:]:
		l = l.strip().split('\t')
		languages.add(l[1])

	return sorted(list(languages))


def get_languages_from_Eng(domains=None):
	with open(index_file, 'r') as inp:
		lines = inp.readlines()
	with open(flores_index_file, 'r') as inp:
		lines += inp.readlines()[1:]

	languages = set()
	for l in lines[1:]:
		if l.strip()[0] != '#':
			l = l.strip().split('\t')
			if l[0] == 'eng':
				if (domains is None) or any([w in domains for w in l[7].strip().split(',')]):
					languages.add(l[1])
	return sorted(list(languages))


def get_mt_languages(domains=None):
	with open(index_file, 'r') as inp:
		lines = inp.readlines()
	with open(flores_index_file, 'r') as inp:
		lines += inp.readlines()[1:]

	languages = set()
	for l in lines[1:]:
		if l.strip()[0] != '#' :
			l = l.strip().split('\t')
			if (l[0] != 'nno'):
				languages.add(l[0])
				languages.add(l[1])
	return sorted(list(languages))


def get_all_language_pairs(domains=None):
	with open(index_file, 'r') as inp:
		lines = inp.readlines()
	with open(flores_index_file, 'r') as inp:
		lines += inp.readlines()[1:]

	languages = set()
	for l in lines[1:]:
		if l.strip()[0] != '#':
			l = l.strip().split('\t')
			if (domains is None) or any([w in domains for w in l[7].strip().split(',')]):
				languages.add((l[0],l[1]))
	return sorted(list(languages))


def get_wilderness_languages():
	with open(wilderness_file, 'r') as inp:
		lines = inp.readlines()

	languages = set()
	for l in lines[1:]:
		l = l.strip().split('\t')
		languages.add(l[1])
	return sorted(list(languages))

def read_wilderness():
	with open(wilderness_file, 'r') as inp:
		lines = inp.readlines()
	d = defaultdict(lambda:0)
	for l in lines[1:]:
		l = l.strip().split('\t')
		iso = l[1]
		val = float(l[9])
		if iso == "eng":
			val -= 3
		d[iso] = val
	return d

def read_wilderness_countries():
	with open(wilderness_countries_file, 'r') as inp:
		lines = inp.readlines()
	d = defaultdict(lambda:0)
	for l in lines:
		l = l.strip().split('\t')
		iso = l[0]
		val = l[1]
		d[iso] = val
	return d

def read_iliteracy_pop():
	with open(literacy_file, 'r') as inp:
		lines = inp.readlines()
	d = defaultdict(lambda:0)
	for l in lines[1:]:
		try:
			l = l.strip().split('\t')
			country = l[0]
			illiteracy = 100 - float(l[1])
			pop = float(l[2])*100/1000000.0
			d[country] = (illiteracy * pop, illiteracy)
		except:
			pass
	return d


def read_BLEUs(domains=None):
	with open(index_file, 'r') as inp:
		lines = inp.readlines()
	with open(flores_index_file, 'r') as inp:
		lines += inp.readlines()[1:]

	d = defaultdict(lambda:0)
	for l in lines[1:]:
		if l.strip() and l.strip()[0] != '#':
			l = l.strip().split('\t')
			if domains:
				if any( [w in domains for w in l[7].strip().split(',')] ):
					d[l[0],l[1]] = max(float(l[2]), d[l[0],l[1]])
			else:
				d[l[0],l[1]] = max(float(l[2]), d[l[0],l[1]])	
	return d


def read_BLEUs_by_year(year=2019):
	year = f"{int(year)}"
	shortyear = year[-2:]
	with open(index_file, 'r') as inp:
		lines = inp.readlines()
	if year == '2021':
		with open(flores_index_file, 'r') as inp:
			lines = inp.readlines()


	d = defaultdict(lambda:0)
	for l in lines[1:]:
		if l.strip() and l.strip()[0] != '#':
			l = l.strip().split('\t')
			if (year in l[4]) or (year in l[5]) or (year in l[6]):
				d[l[0],l[1]] = max(float(l[2]), d[l[0],l[1]])
			elif year == '2019' and l[6].strip() == 'internal':
				d[l[0],l[1]] = max(float(l[2]), d[l[0],l[1]])
			elif 'arxiv' in l[4]:
				temp = l[4].split('/')[-1][:2]
				if temp == shortyear:
					d[l[0],l[1]] = max(float(l[2]), d[l[0],l[1]])
			elif 'anthology' in l[4]:
				temp = l[4].split('/')[-1][1:3]
				if temp == shortyear:
					d[l[0],l[1]] = max(float(l[2]), d[l[0],l[1]])
				if '2020.acl-main' in l[4] and year == '2020':
					d[l[0],l[1]] = max(float(l[2]), d[l[0],l[1]])
			elif year=='2021' and ('FLORES' in l[3]):
				d[l[0],l[1]] = max(float(l[2]), d[l[0],l[1]])

	return d


def read_triangulated_BLEUs():
	with open(triangulation_file, 'r') as inp:
		lines = inp.readlines()

	d = defaultdict(lambda:0)
	for l in lines:
		if l.strip() and l.strip()[0] != '#':
			l = l.strip().split('\t')
			d[l[0],l[1]] = max(float(l[2]), d[l[0],l[1]])	
	return d

def read_dep(metric='uas', system='udp'):
	with open(dep_file, 'r') as inp:
		lines = inp.readlines()

	d = defaultdict(lambda:0)
	for l in lines[1:]:
		if l.strip():
			l = l.strip().split('\t')
			if metric == 'uas':
				if system == 'udp':
					d[l[0]] = float(l[1])
				elif system == 'udf':
					d[l[0]] = float(l[3])
			elif metric == 'las':
				if system == 'udp':
					d[l[0]] = float(l[2])
				elif system == 'udf':
					d[l[0]] = float(l[4])
	return d

def read_sig(year='all',system='CULing-01-0',include_isolating=True):
	d = defaultdict(lambda:0)
	if year == '20' or year=='all':
		with open(sig_file, 'r') as inp:
			lines = inp.readlines()

		for l in lines[1:]:
			if l.strip():
				l = l.strip().split('\t')
				if system == 'CULing-01-0':
					d[l[0]] = float(l[1])
				elif system == 'deepspin-02-1':
					d[l[0]] = float(l[2])
				elif system == 'uiuc-01-0':
					d[l[0]] = float(l[3])
	if year == '19'  or year=='all':
		with open(sig19_file, 'r') as inp:
			lines = inp.readlines()
		for l in lines:
			if l.strip():
				l = l.strip().split('\t')
				#print(l)
				if float(l[1])/100 > d[l[0]]:
					d[l[0]] = float(l[1])/100
	if year == '18' or year=='all':
		with open(sig18_file, 'r') as inp:
			lines = inp.readlines()
		for l in lines:
			if l.strip():
				l = l.strip().split('\t')
				if float(l[1])/100 > d[l[0]]:
					d[l[0]] = float(l[1])/100
	if year == '17' or year=='all':
		with open(sig17_file, 'r') as inp:
			lines = inp.readlines()
		for l in lines:
			if l.strip():
				l = l.strip().split('\t')
				if float(l[1])/100 > d[l[0]]:
					d[l[0]] = float(l[1])/100
	if year == '16' or year=='all':
		with open(sig16_file, 'r') as inp:
			lines = inp.readlines()
		for l in lines:
			if l.strip():
				l = l.strip().split('\t')
				if float(l[1])/100 > d[l[0]]:
					d[l[0]] = float(l[1])/100
	if include_isolating:
		with open(sig_isolating_file, 'r') as inp:
			lines = inp.readlines()
		for l in lines:
			if l.strip():
				l = l.strip().split('\t')
				if float(l[1]) > d[l[0]]:
					d[l[0]] = float(l[1])

	return d


def read_human_evals(domains=None):
	raise NotImplementedError("No data on human evals so not implemented")

def read_post_editing_evals(domains=None):
	raise NotImplementedError("No data on post-editing evals so not implemented")


def read_xnli_acc():
	with open(xnli_file, 'r') as inp:
		lines = inp.readlines()

	d = defaultdict(lambda:0)
	for l in lines[1:]:
		l = l.strip().split('\t')
		d[l[0]] = float(l[1])
	return d

read_XNLI_acc = read_xnli_acc

def read_qa_acc():
	with open(qa_file, 'r') as inp:
		lines = inp.readlines()

	d = defaultdict(lambda:0)
	for l in lines[1:]:
		l = l.strip().split('\t')
		d[l[0]] = float(l[1])
	#print(d)
	return d
read_QA_acc = read_qa_acc

def read_number_of_papers(domains=None):
	with open(index_file, 'r') as inp:
		lines = inp.readlines()

	d = defaultdict(lambda:0)
	for l in lines[1:]:
		if l.strip() and l[0].strip()!='#':
			l = l.strip().split('\t')
			if domains:
				if any( [w in domains for w in l[7].strip().split(',')] ):
					d[l[0],l[1]] += 1 
			else:
				d[l[0],l[1]] += 1
	return d

def read_number_of_internal_papers(domains=None):
	with open(index_file, 'r') as inp:
		lines = inp.readlines()

	d = defaultdict(lambda:0)
	for l in lines[1:]:
		if l.strip():
			l = l.strip().split('\t')
			if len(l) > 3:
				if domains:
					if any( [w in domains for w in l[7].strip().split(',')] ) and l[6].strip()=='internal':
						d[l[0],l[1]] += 1 
				elif l[6].strip()=='internal':
					d[l[0],l[1]] += 1
	return d


def triangulate(acc):
	# First recover all the languages
	alllangs = set( [ l[0] for l in acc ] + [ l[1] for l in acc ] + ['eng'] )
	# Store original dict
	original_dict = defaultdict(lambda:0)
	for key in acc:
		original_dict[key] = acc[key]
	
	# For storing the pivot
	pivot = {}
	for l1 in alllangs:
		for l2 in alllangs:
			pivot[l1,l2] = []
	
	
	#Pivot once
	for l1 in alllangs:
		for l2 in alllangs:
			for l3 in alllangs:
				if l1 != l2 and l2 != l3:
					if original_dict[l1,l2] < original_dict[l1,l3] * original_dict[l3,l2]:
						acc[l1,l2] = original_dict[l1,l3] * original_dict[l3,l2]
						pivot[l1,l2] = [l3]


	#Pivot twice
	for l1 in alllangs:
		for l2 in alllangs:
			for l3 in alllangs:
				for l4 in alllangs:
					if l1 != l2 and l2 != l3 and l3 != l4:
						if acc[l1,l2] < original_dict[l1,l3] * original_dict[l3,l4] * original_dict[l4,l2]:
							# Weird because normalizing does the last operation when recovering it. TO DO
							acc[l1,l2] = original_dict[l1,l3] * original_dict[l3,l4]  * original_dict[l4,l2]
							pivot[l1,l2] = [l3,l4]

	#Pivot once through estimates
	#pivot = {}
	for l1 in alllangs:
		for l2 in alllangs:
			for l3 in alllangs:
				if l1 != l2 and l2 != l3:
					if acc[l1,l2] < acc[l1,l3] * acc[l3,l2]:
						acc[l1,l2] = acc[l1,l3] * acc[l3,l2]
						pivot[l1,l2] = pivot[l1,l3] + [l3] + pivot[l3,l2]
