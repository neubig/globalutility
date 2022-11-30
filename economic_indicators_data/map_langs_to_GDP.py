from collections import defaultdict

NOMINAL_GDP = "NOMINAL_GDP.tsv"
with open(NOMINAL_GDP) as inp:
    lines = inp.readlines()

c2gdp = {}
for l in lines:
    l = l.strip().split("\t")
    c = l[1].strip()
    gdp = l[2]
    c2gdp[c] = int(gdp)

with open("country_populations.tsv") as inp:
    lines = inp.readlines()

c2pop = {}
for l in lines:
    l = l.strip().split("\t")
    country = l[1]
    pop = int(l[2])
    c2pop[country] = pop

with open("CountryCodes.tab") as inp:
    lines = inp.readlines()

c2code = {}
c2area = {}
code2c = {}
for l in lines:
    l = l.strip().split("\t")
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
    l = l.strip().split("\t")
    if len(l) == 2:
        iso = l[0]
        pop = l[1].split()[0].replace(",", "")
        if "A macrolanguage" in l[1]:
            pop = l[1].split()[-1].replace(",", "")
        try:
            pop = int(pop)
        except:
            pop = 0
            pass
        if pop:
            iso2pop[iso] = pop
            iso2macro[iso] = "macrolanguage" in l[1]


iso2country = defaultdict(lambda: set())
with open("LanguageIndex.tab") as inp:
    lines = inp.readlines()

for l in lines[1:]:
    l = l.strip().split("\t")
    iso = l[0]
    country = l[1]
    iso2country[iso].add(country)
    if iso in "fat,twi".split(","):
        iso2country["aka"].add(country)
    elif (
        iso
        in "aao,abh,abv,acm,acq,acw,acx,acy,adf,aeb,aec,afb,ajp,apc,apd,arb,arq,ars,ary,arz,auz,avl,ayh,ayl,ayn,ayp,pga,shu,ssh".split(
            ","
        )
    ):
        iso2country["ara"].add(country)
    elif iso in "ayr,ayc".split(","):
        iso2country["aym"].add(country)
    elif iso in "azj,azb".split(","):
        iso2country["aze"].add(country)
    elif iso in "bgp,bcc,bgn".split(","):
        iso2country["bal"].add(country)
    elif iso in "bcl,bto,cts,bln,fbl,lbl,rbl,ubl,bhk".split(","):
        iso2country["bik"].add(country)
    elif iso in "ebk,lbk,obk,rbk,vbk".split(","):
        iso2country["bnc"].add(country)
    elif iso in "bxu,bxm,bxr".split(","):
        iso2country["bua"].add(country)
    elif iso in "mhr,mrj".split(","):
        iso2country["chm"].add(country)
    elif iso in "crm,crl,crk,crj,csw,cwd,nsk,moe,atj,crg,ojs,ojw".split(","):
        iso2country["cre"].add(country)
    elif iso in "umu,unm".split(","):
        iso2country["del"].add(country)
    elif iso in "scs,xsl".split(","):
        iso2country["den"].add(country)
    elif iso in "dip,diw,dib,dks,dik".split(","):
        iso2country["din"].add(country)
    elif iso in "dgo,xnr".split(","):
        iso2country["doi"].add(country)
    elif iso in "ekk,vro,faa".split(","):
        iso2country["est"].add(country)
    elif iso in "prs,pes".split(","):
        iso2country["fas"].add(country)
    elif iso in "fub,fui,fue,fuq,ffm,fuv,fuc,fuf,fuh".split(","):
        iso2country["ful"].add(country)
    elif iso in "bdt,gbp,gbq,gmm,gya,gso,mdo".split(","):
        iso2country["gba"].add(country)
    elif iso in "esg,gno,wsg,ggo".split(","):
        iso2country["gon"].add(country)
    elif iso in "gry,grv,gec,gbo,grj".split(","):
        iso2country["grb"].add(country)
    elif iso in "nhd,gui,gun,gug,gnw".split(","):
        iso2country["grn"].add(country)
    elif iso in "hdn,hax".split(","):
        iso2country["hai"].add(country)
    elif iso in "bos,hrv,cnr,srp".split(","):
        iso2country["hbs"].add(country)
    elif (
        iso
        in "hmc,hmm,cqd,hme,hmq,muq,hmj,mww,hnj,hrm,hmd,hml,huj,hmi,hmp,hea,sfm,hmy,hma,hms,hmg,hmh,hmw,hmz,mmr,blu".split(
            ","
        )
    ):
        iso2country["hmn"].add(country)
    elif iso in "ike,ikt".split(","):
        iso2country["iku"].add(country)
    elif iso in "esi,esk".split(","):
        iso2country["ipk"].add(country)
    elif iso in "yhd,aju,yud,ajt,jye,kaa".split(","):
        iso2country["jrb"].add(country)
    elif iso in "knc,kby,krt,bms,kbl".split(","):
        iso2country["kau"].add(country)
    elif iso in "eyo,sgc,enb,niq,oki,pko,spy,tec,tuy".split(","):
        iso2country["kln"].add(country)
    elif iso in "gom,knn".split(","):
        iso2country["kok"].add(country)
    elif iso in "koi,kpv".split(","):
        iso2country["kom"].add(country)
    elif iso in "kng,ldi,kwy".split(","):
        iso2country["kon"].add(country)
    elif iso in "gkp,xpe".split(","):
        iso2country["kpe"].add(country)
    elif iso in "ckb,kmr,sdh".split(","):
        iso2country["kur"].add(country)
    elif iso in "jat,xhe,hno,phr,skr,hnd,pnb,pmu".split(","):
        iso2country["lah"].add(country)
    elif iso in "ltg,lvs".split(","):
        iso2country["lav"].add(country)
    elif iso in "bxk,nle,ida,lkb,lko,lks,rag,lri,lrm,nyd,lsm,lts,lto,lwg".split(","):
        iso2country["luy"].add(country)
    elif iso in "emk,mwk,mku,mnk,msc,mlq".split(","):
        iso2country["man"].add(country)
    elif iso in "xmv,bhr,msh,bmm,plt,skg,bzc,tkg,tdx,txy,xmw,bjq".split(","):
        iso2country["mlg"].add(country)
    elif iso in "khk,mvf".split(","):
        iso2country["mon"].add(country)
    elif (
        iso
        in "btj,mfb,bjn,bve,kxd,bvu,pse,coa,liw,dup,hji,ind,jak,jax,vkk,meo,kvr,mqg,kvb,lce,lcf,zlm,xmm,min,mui,zmi,max,orn,ors,mfa,pel,msi,zsm,tmw,vkt,urk,mly".split(
            ","
        )
    ):
        iso2country["msa"].add(country)
    elif iso in "dhd,rwr,mve,wry,mtr,swv".split(","):
        iso2country["mwr"].add(country)
    elif iso in "dty,npi".split(","):
        iso2country["nep"].add(country)
    elif iso in "nob,nno".split(","):
        iso2country["nor"].add(country)
    elif iso in "ciw,ojb,ojc,ojg,ojs,ojw,otw,alq,pot,crg".split(","):
        iso2country["oji"].add(country)
    elif iso in "ory,spv".split(","):
        iso2country["ori"].add(country)
    elif iso in "gax,hae,orc,gaz,paa".split(","):
        iso2country["orm"].add(country)
    elif iso in "pst,pbu,pbt".split(","):
        iso2country["pus"].add(country)
    elif (
        iso
        in "qva,qxu,quy,qvc,qvl,qud,qxr,quk,qug,qxc,qxa,qwc,qwa,quz,qve,qub,qvh,qwh,qvw,qvi,qxw,quf,qvj,qvm,qvo,qul,qvn,qxn,qvz,qvp,qxh,qxp,qxl,qvs,qxt,qus,qws,quh,qxo,qup,quw,qur,qux,cqu".split(
            ","
        )
    ):
        iso2country["que"].add(country)
    elif iso in "bgq,gda,gju,hoj,mup,wbr".split(","):
        iso2country["raj"].add(country)
    elif iso in "rmn,rml,rmc,rmf,rmo,rmy,rmw,emx,rge,rmd,rme,rmg,rmi,rmr,rmu,rsb".split(
        ","
    ):
        iso2country["rom"].add(country)
    elif iso in "aae,aat,aln,als".split(","):
        iso2country["sqi"].add(country)
    elif iso in "sro,sdn,src,sdc".split(","):
        iso2country["srd"].add(country)
    elif iso in "swc,swh".split(","):
        iso2country["swa"].add(country)
    elif iso in "aii,cld".split(","):
        iso2country["syr"].add(country)
    elif iso in "thv,taq,ttq,thz".split(","):
        iso2country["tmh"].add(country)
    elif iso in "uzn,uzs".split(","):
        iso2country["uzb"].add(country)
    elif iso in "ydd,yih".split(","):
        iso2country["yid"].add(country)
    elif (
        iso
        in "zaq,zpo,zoo,zaf,zad,zpv,zpc,zca,zps,zpp,zte,zpg,ztu,zai,zpa,zpl,ztl,ztp,zpy,zam,zaw,zpm,zac,zao,zpe,zpj,ztq,zar,ztm,zpx,zab,zpf,zpt,ztn,zpn,zpi,zpr,zas,zaa,zpd,zsr,zat,ztt,zpz,zts,zpk,zph,zax,ztg,zpu,zae,zty,zav,zpb,ztx,zpw,zpq,ztc,xzp".split(
            ","
        )
    ):
        iso2country["zap"].add(country)
    elif (
        iso
        in "zch,zhd,zeh,zgb,zgn,zln,zlj,zlq,zgm,zhn,zqe,zyg,zyb,zyn,zyj,zzj,ccx,ccy".split(
            ","
        )
    ):
        iso2country["zha"].add(country)
    elif iso in "cdo,cjy,cmn,cnp,cpx,csp,czh,czo,gan,hak,hsn,lzh,mnp,nan,wuu,yue".split(
        ","
    ):
        iso2country["zho"].add(country)
    elif iso in "diq,kiu".split(","):
        iso2country["zza"].add(country)


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
    l = l.strip().split("\t")
    iso = l[0]
    countries = l[1].split(",")
    if iso != "epo":
        print(iso, countries)
        countrycodes = set()
        SumGDP = 0
        for c in countries:
            if "-" in c:
                c = c.split("-")
                country = c[0]
                weight = float(c[1])
            else:
                country = c
                weight = 1
            if country in c2gdp:
                SumGDP += weight * c2gdp[country]
            else:
                print(f"Missing Country: {country}")

        final[iso] = [iso, ",".join(countries), str(iso2pop[iso]), f"{SumGDP:.2f}"]


c = 0
for iso in iso2pop:
    if iso in final:
        continue

    langpop = iso2pop[iso]
    countries = iso2country[iso]
    # print(iso)
    # print(langpop)
    SumGDP = 0
    country_names = []
    for country_code in countries:
        if country_code in code2c:
            country_name = code2c[country_code]
            if country_name in c2pop and country_name in c2gdp:
                # print(f"{country_name}: {c2pop[country_name]}")
                if c2pop[country_name] > langpop:
                    weight = langpop / c2pop[country_name]
                else:
                    weight = 1

                SumGDP += weight * c2gdp[country_name]
                country_names.append(f"{country_name}-{weight:.5f}")

    final[iso] = [iso, ",".join(country_names), str(iso2pop[iso]), f"{SumGDP:.2f}"]
    # print(final[iso])


isos = sorted(list(final.keys()))


with open("languages_to_economic.tsv", "w") as op:
    op.write("ISO 639-3\tcountries (weighted)\ttotal population\ttotal GDP\n")
    for iso in isos:
        op.write("\t".join(final[iso]) + "\n")
