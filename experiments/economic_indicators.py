from collections import defaultdict
import os
import csv
import traceback
from operator import itemgetter

ETHNOLOGUE_COUNTRY_CODES = "/Users/antonios/Desktop/research/PNAS_Fairness/globalutility/experiments/economic_indicators_data/CountryCodes.tab"
ETHNOLOGUE_LANGUAGE_INDEX = "/Users/antonios/Desktop/research/PNAS_Fairness/globalutility/experiments/economic_indicators_data/LanguageIndex.tab"
LANGUAGE_MAPPINGS = "/Users/antonios/Desktop/research/PNAS_Fairness/globalutility/experiments/economic_indicators_data/language_mappings.txt"
DATA_DIR = "/Users/antonios/Desktop/research/PNAS_Fairness/globalutility/experiments/economic_indicators_data/wits_en_trade_summary_allcountries_allyears"
LANGUAGE_TO_COUNTRY_INDEX = "/Users/antonios/Desktop/research/PNAS_Fairness/globalutility/experiments/economic_indicators_data/language_to_countries_map_small.txt"
LANGUAGE_TO_COUNTRY_INDEX_WEIGHTED = "/Users/antonios/Desktop/research/PNAS_Fairness/globalutility/experiments/economic_indicators_data/language_to_countries_map_weighted.txt"
NOMINAL_GDP = "/Users/antonios/Desktop/research/PNAS_Fairness/globalutility/experiments/economic_indicators_data/NOMINAL_GDP.tsv"

def read_country_mappings(reverse=False):
	with open(LANGUAGE_MAPPINGS) as inp:
		lines = inp.readlines()
	d = {}
	for l in lines:
		l = l.strip().split('\t')
		if reverse:
			d[l[0].strip()] = l[1].strip()
		else:
			d[l[1].strip()] = l[0].strip()
	return d


def read_language_to_country_maps():
	typ = read_country_mappings(reverse=True)
	with open(LANGUAGE_TO_COUNTRY_INDEX) as inp:
		lines = inp.readlines()
	d = {}
	for l in lines:
		l = l.strip().split('\t')
		inside = l[1].strip().split(',')
		for i,ex in enumerate(inside):
			if ex in typ:
				#print("found one!", ex, typ[ex])
				inside[i] == typ[ex]
		d[l[0]] = inside
	return d

def read_language_to_country_maps_weighted():
	typ = read_country_mappings(reverse=True)
	with open(LANGUAGE_TO_COUNTRY_INDEX_WEIGHTED) as inp:
		lines = inp.readlines()
	d = defaultdict(lambda:[])
	for l in lines:
		l = l.strip().split('\t')
		if len(l) > 1:
			inside = l[1].strip().split(',')
			for i,ex in enumerate(inside):
				if '-' in ex:
					temp = ex.split('-')
					ex = temp[0]
					weight = float(temp[1])
				else:
					weight = 1.0
				if ex in typ:
					ex = typ[ex]
				inside[i] = (ex,weight)
			d[l[0]] = inside

	return d

def get_ethnologue_countries():
	with open(ETHNOLOGUE_COUNTRY_CODES) as inp:
		lines = inp.readlines()

	d = {}
	d2 = {}
	for l in lines:
		l = l.strip().split('\t')
		c_id = l[0].strip()
		c_name = l[1].strip()
		d[c_id] = c_name
		d2[c_name] = c_id
	return d, d2

def get_ethnologue_languages():
	with open(ETHNOLOGUE_LANGUAGE_INDEX) as inp:
		lines = inp.readlines()

	d = {}
	for l in lines:
		l = l.strip().split('\t')
		l_id = l[0].strip()
		c_id = l[1].strip()
		if l_id in d:
			if c_id not in d[l_id]:
				d[l_id].append(c_id)
		else:
			d[l_id] = [c_id]
	return d


# Needed for noisy WITS data
def helper_for_years(lines, indicator_type, indicator, year=2017):
	if year == 2017:
		ind = 5
	else:
		ind = 5 + 2017 - year
	d = {}
	d['year'] = year
	remainder = 100.0

	if 'absolute' in indicator:
		try:
			for l in lines[1:]:
				if l[1].strip() == "World" and l[2].strip() == "All Products" and l[3].strip() == indicator_type and ("in US$ Mil" in l[4]):
					if l[ind].strip():
						d['world'] = float(l[ind].strip())
						remainder = d['world']
						break
		except:
			print("Error in world")

		if remainder == 100.0:
			d['others'] = remainder
			return d


	for l in lines[1:]:
		#l = l.strip().split(',')
		if l[ind].strip():
			#print("came in 1")
			if l[2].strip() == "All Products" and l[3] == indicator_type and l[1].strip() != 'World':
				#print("came in 2")
				if indicator=="Top 5" and ("Partner share" in l[4]):
					partner = l[1].strip()
					percentage = float(l[ind].strip())
					remainder -= percentage
					d[partner] = percentage
				elif indicator=="Top 5 absolute" and ("Trade (US$ Mil)" in l[4]):
					partner = l[1].strip()
					percentage = float(l[ind].strip())
					remainder -= percentage
					d[partner] = percentage
	d['others'] = remainder
	return d


def read_csv_file(f, indicator_type="Import", indicator="Top 5"):
	try:
		#print("Reading ", f)
		with open(f, newline='', encoding="ISO-8859-1") as inp:
			reader = csv.reader(inp)
			lines = [line for line in reader]

		country_abbreviation = f.split('/')[-1].split('_')[1]
		country = lines[2][0].strip()
		#print(country_abbreviation, country)
		if not country.strip():
			return -1, -1, -1

		year = 2017
		d = helper_for_years(lines, indicator_type, indicator, year)
		while d['others'] == 100:
			year -= 1
			if year < 2000:
				return -1, -1, -1
			d = helper_for_years(lines, indicator_type, indicator, year)
		
		return d, country, country_abbreviation
	except Exception as exc:
		print(traceback.format_exc())
		print(exc)
		print(f"Error in {f}")
		return -1, -1, -1


def read_economic_indicators(languages=[], ind_type="Import", ind="Top 5 absolute"):
	# expect a set of languages
	N = len(languages)
	print(f"Reading economic indicators for {N} languages: {languages}")
	data = {}
	countries = set()
	for f in os.listdir(DATA_DIR):
		d, country, country_abbreviation = read_csv_file(os.path.join(DATA_DIR,f), indicator_type=ind_type, indicator=ind)
		if d == -1:
			print(f)
		else:
			data[country] = d
			countries.add((country, country_abbreviation))
		
	country_map = read_country_mappings()
	ethnologue_countries, ethn_c_name2id = get_ethnologue_countries()
	lang_index = get_ethnologue_languages()

	lang2country = read_language_to_country_maps()


	newdata = defaultdict(lambda:0)
	for l1 in languages:
		for l2 in languages:
			if l1 != l2:
				num_countries1 = len(lang2country[l1])
				num_countries2 = len(lang2country[l2])
				countries1 = lang2country[l1]
				countries2 = lang2country[l2]
				denom = num_countries1 * num_countries2
				for country1 in countries1:
					if country1 in data:
						for country2 in countries2:
							if country2 in data[country1]:
								if (l1,l2) in newdata:
									newdata[(l1,l2)] += (data[country1][country2] / denom)
								else:
									newdata[(l1,l2)] = (data[country1][country2] / denom)
							else:
								# Gotta do an approximation
								if (l1,l2) in newdata:
									newdata[(l1,l2)] += (data[country1]['others'] / ((N-5) * denom))
								else:
									newdata[(l1,l2)] = (data[country1]['others'] / ((N-5) * denom))

				if (l1,l2) not in newdata:
					newdata[(l1,l2)] = 100.0/(N-1)

	return newdata


def read_absolute_economic_indicators2(languages=[], ind_type="Import", ind="Top 5 absolute"):
	# expect a set of languages
	N = len(languages)
	print(f"Reading economic indicators for {N} languages: {languages}")
	data = {}
	countries = set()
	for f in os.listdir(DATA_DIR):
		d, country, country_abbreviation = read_csv_file(os.path.join(DATA_DIR,f), indicator_type=ind_type, indicator=ind)
		if d == -1:
			print(f"{d}:{f}")
		else:
			data[country] = d
			countries.add((country, country_abbreviation))
		
	country_map = read_country_mappings(reverse=True)
	ethnologue_countries, ethn_c_name2id = get_ethnologue_countries()
	lang_index = get_ethnologue_languages()

	lang2country = read_language_to_country_maps_weighted()

	newdata = defaultdict(lambda:0)
	for l1 in languages:
		for l2 in languages:
			if l1 != l2:
				num_countries1 = len(lang2country[l1])
				num_countries2 = len(lang2country[l2])
				countries1 = [k[0] for k in lang2country[l1]]
				countryweights1 = [k[1] for k in lang2country[l1]]
				countries2 = [k[0] for k in lang2country[l2]]
				countryweights2 = [k[1] for k in lang2country[l2]]
				for c1,country1 in enumerate(countries1):
					if country1 not in data:
						if country1 in country_map:
							country1 = country_map[country1]
					if country1 in data:
						for c2,country2 in enumerate(countries2):
							if country2 not in data[country1]:
								if country2 in country_map:
									country2 = country_map[country2]
							if country2 in data[country1]:
								newdata[(l1,l2)] += (data[country1][country2])
							else:
								newdata[(l1,l2)] += (data[country1]['others']/ (N-5))
				
				if (l1,l2) not in newdata:
					newdata[(l1,l2)] = 0

	return newdata

def read_nominal_gdp(languages=[]):
	# expect a set of languages
	N = len(languages)
	print(f"Reading gdp for {N} languages: {languages}")
	data = {}
	with open(NOMINAL_GDP) as inp:
		lines = inp.readlines()
	for l in lines:
		l = l.strip().split('\t')
		data[l[1].strip()] = int(l[2])
	country_map = read_country_mappings(reverse=True)
	ethnologue_countries, ethn_c_name2id = get_ethnologue_countries()
	lang_index = get_ethnologue_languages()
	lang2country = read_language_to_country_maps_weighted()
	newdata = defaultdict(lambda:0)
	for l1 in languages:
		num_countries1 = len(lang2country[l1])
		countries1 = [k[0] for k in lang2country[l1]]
		countryweights1 = [k[1] for k in lang2country[l1]]
		for c1,country1 in enumerate(countries1):
			#if country1 not in data:
			#	print(l1,country1)
			#	if country1 in country_map:
			#		country1 = country_map[country1]
			if country1 in data:
				newdata[l1] += data[country1]*countryweights1[c1]
			else:
				print(l1,country1)
			
	return newdata

def read_absolute_economic_indicators(languages=[], ind_type="Import", ind="Top 5 absolute"):
	# expect a set of languages
	N = len(languages)
	print(f"Reading economic indicators for {N} languages: {languages}")
	data = {}
	countries = set()
	for f in os.listdir(DATA_DIR):
		d, country, country_abbreviation = read_csv_file(os.path.join(DATA_DIR,f), indicator_type=ind_type, indicator=ind)
		if d == -1:
			print(f"{d} {f}")
		else:
			data[country] = d
			countries.add((country, country_abbreviation))
	
	country_map = read_country_mappings(reverse=True)
	ethnologue_countries, ethn_c_name2id = get_ethnologue_countries()
	lang_index = get_ethnologue_languages()

	lang2country = read_language_to_country_maps_weighted()

	newdata = defaultdict(lambda:0)
	for l1 in languages:
		for l2 in languages:
			if l1 != l2:
				num_countries1 = len(lang2country[l1])
				num_countries2 = len(lang2country[l2])
				countries1 = [k[0] for k in lang2country[l1]]
				countryweights1 = [k[1] for k in lang2country[l1]]
				countries2 = [k[0] for k in lang2country[l2]]
				countryweights2 = [k[1] for k in lang2country[l2]]
				for c1,country1 in enumerate(countries1):
					if country1 not in data:
						if country1 in country_map:
							country1 = country_map[country1]
					if country1 in data:
						for c2,country2 in enumerate(countries2):
							if country2 not in data[country1]:
								if country2 in country_map:
									country2 = country_map[country2]
							if country2 in data[country1]:
								newdata[(l1,l2)] += (data[country1][country2]*countryweights1[c1]*countryweights2[c2])
							else:
								newdata[(l1,l2)] += (data[country1]['others']*countryweights1[c1] / (N-5))
				
				if (l1,l2) not in newdata:
					newdata[(l1,l2)] = 0

	return newdata
