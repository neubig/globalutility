from collections import defaultdict

NOMINAL_GDP = "NOMINAL_GDP.tsv"
with open(NOMINAL_GDP) as inp:
	lines = inp.readlines()

c2gdp = {}
for l in lines:
	l = l.strip().split('\t')
	c = l[1].strip()
	gdp = l[2]
	c2gdp[c] = int(gdp)

with open("country_populations.tsv") as inp:
	lines = inp.readlines()

c2pop = {}
for l in lines:
	l = l.strip().split('\t')
	country = l[1]
	pop = int(l[2])
	c2pop[country] = pop 

with open("CountryCodes.tab") as inp:
	lines = inp.readlines()

c2code = {}
c2area = {}
code2c = {}
for l in lines:
	l = l.strip().split('\t')
	code = l[0]
	country = l[1]
	area = l[2]
	if country not in c2pop:
		print(f"Error: {country}")
	elif country not in c2gdp:
		print(f"Error2: {country}")
	else:
		c2code[country] = code
		code2c[code] = country
		c2area[country] = area


iso2pop = {}
iso2macro = {}
with open("../populations/ethnologue20b.tsv") as inp:
	lines = inp.readlines()

for l in lines:
	l = l.strip().split('\t')
	if len(l) == 2:
		iso = l[0]
		pop = l[1].split()[0].replace(",","")
		if "A macrolanguage" in l[1]:
			pop = l[1].split()[-1].replace(",","")
		try:
			pop = int(pop)
		except:
			pop = 0
			pass
		if pop:
			iso2pop[iso] = pop
			iso2macro[iso] = "macrolanguage" in l[1]
			

iso2country = defaultdict(lambda:set())
with open("LanguageIndex.tab") as inp:
	lines = inp.readlines()

for l in lines[1:]:
	l = l.strip().split('\t')
	iso = l[0]
	country = l[1]
	iso2country[iso].add(country)
	if iso in 'fuc,fuf,ffm,fue,fuh,fuq,fuv,fub,fui'.split(','):
		iso2country['ful'].add(country)
	elif iso in 'emk,mwk,mku,mnk,msc,mlq'.split(','):
		iso2country['man'].add(country)
	elif iso in 'nhd,gui,gun,gug,gnw'.split(','):
		iso2country['grn'].add(country)
	elif iso in 'gom,knn'.split(','):
		iso2country['kok'].add(country)
	elif iso in 'kng,ldi,kwy'.split(','):
		iso2country['kon'].add(country)
	elif iso in 'buk,nle,ida,lkb,lko,lks,rag,lri,lrm,nyd,lsm,lts,lto,lwg'.split(','):
		iso2country['luy'].add(country)
	elif iso in 'jat,xhe,hno,phr,skr,hnd,pnb'.split(','):
		iso2country['lah'].add(country)
	elif iso in 'qva,qxu,quy,qvc,qvl,qud,qxr,quk,qug,qxc,qxa,qwc,qwa,quz,qve,qub,qvh,qvw,qwh,qvi,qxw,quf,qvj,qvm,qvo,qul,qvn,qxn,qvz,qvp,qxh,qxp,qxl,qvs,qxt,qus,qws,quh,qho,qup,quw,qur,qux'.split(','):
		iso2country['que'].add(country)
	elif iso in 'hmc,hmm,cqd,hme,hmq,hmj,muq,mww,hnj,hrm,hmd,hml,huj,hmi,hmp,hea,sfm,hmy,hma,hms,hmg,hmh,hmw,hmz,mmr'.split(','):
		iso2country['hmn'].add(country)
	elif iso in 'zch,zhd,zeh,zgb,zgn,zln,zlj,zlq,zgm,zhn,zqe,zyg,zyb,zyn,zyj,zzh'.split(','):
		iso2country['zha'].add(country)
	elif iso in 'bgq,gda,gju,hoj,mup,wbr'.split(','):
		iso2country['raj'].add(country)
	elif iso in 'rmn,rml,rmc,rmf,rmo,rmy,rmw'.split(','):
		iso2country['rom'].add(country)


print(f"iso2country: {list(iso2country.keys())[:5]}")
print(f"iso2pop: {list(iso2pop.keys())[:5]}")
print(f"iso2pop: {list(iso2pop.keys())[:5]}")
print(f"code2c: {list(code2c.keys())[:5]}")
print(f"c2pop: {list(c2pop.keys())[:5]}")
print(f"c2gdp: {list(c2gdp.keys())[:5]}")




final = {}

with open("language_to_countries_map_weighted.txt") as inp:
	lines = inp.readlines()

for l in lines:
	l = l.strip().split('\t')
	iso = l[0]
	countries = l[1].split(',')
	if iso != 'epo':
		print(iso, countries)
		countrycodes = set()
		SumGDP = 0
		for c in countries:
			if '-' in c:
				c = c.split('-')
				country = c[0]
				weight = float(c[1])
			else:
				country = c
				weight = 1
			if country in c2gdp:
				SumGDP += weight * c2gdp[country]
			else:
				print(f"Missing Country: {country}")

		final[iso] = [iso, ','.join(countries), str(iso2pop[iso]), f"{SumGDP:.2f}"]


c = 0
for iso in iso2pop:
	if iso in final:
		continue

	langpop = iso2pop[iso]
	countries = iso2country[iso]
	#print(iso)
	#print(langpop)
	SumGDP = 0
	country_names = []
	for country_code in countries:
		if country_code in code2c:
			country_name = code2c[country_code]
			if country_name in c2pop and country_name in c2gdp:
				#print(f"{country_name}: {c2pop[country_name]}")
				if c2pop[country_name] > langpop:
					weight = langpop/c2pop[country_name]
				else:
					weight = 1

				SumGDP += weight * c2gdp[country_name]
				country_names.append(f"{country_name}-{weight:.5f}")

	final[iso] = [iso, ','.join(country_names), str(iso2pop[iso]), f"{SumGDP:.2f}"]
	#print(final[iso])


isos = sorted(list(final.keys()))


with open("languages_to_economic.tsv", 'w') as op:
	op.write('ISO 639-3\tcountries (weighted)\ttotal population\ttotal GDP\n')
	for iso in isos:
		op.write('\t'.join(final[iso])+'\n')
