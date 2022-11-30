import pdftotext
import os
import numpy as np

years = np.arange(2010, 2020)

## Uncomment the below to choose the conference
## It provides the number of long and short papers per year

conferences_l = [f"acl{y}" for y in years]
long_papers = [161, 165, 112, 175, 148, 175, 232, 196, 257, 661]

conferences_s = [f"acl{y}" for y in years]
short_papers = [71, 129, 77, 155, 140, 145, 98, 108, 126]

# conferences_l = [f'emnlp{y}' for y in years]
# long_papers = [125,150,140,206,227,313,265,324,550,682]

# conferences_s = [f'emnlp{y}' for y in years]
# short_papers = [71,129,77,155,140,145,98,108,126]

# conferences_l = [f'naacl{y}' for y in years]
# long_papers = [147, 98, 141, 187, 182, 206, 424]

# conferences_s = ['naacl2018']
# short_papers = [126]

# years = [2012, 2014, 2017]
# conferences_l = [f'eacl{y}' for y in years]
# long_papers = [86,79,120]

# conferences_s = ['eacl2017']
# short_papers = [121]

# conferences = ['aacl2020', 'acl2020', 'acl2019']
# papers = [93,773,661]

for conf, num in zip(conferences_l[1:], long_papers[1:]):
    year = conf[-4:]
    year2 = year[-2:]
    conf_name = conf[:-4]
    if conf_name == "acl":
        conf_id = "P"
    elif conf_name == "emnlp":
        conf_id = "D"
    elif conf_name == "naacl":
        conf_id = "N"
    elif conf_name == "eacl":
        conf_id = "E"

    try:
        os.mkdir(f"text/{conf}")
        os.mkdir(f"pdfs/{conf}")
    except:
        pass
    print(conf, conf_name)
    print(year, year2)
    for i in range(1, num + 1):
        try:
            print(i)
            j = 1000 + i
            command = f"wget https://www.aclweb.org/anthology/{conf_id}{year2}-{j}.pdf"
            os.system(command)
            command = f"mv {conf_id}{year2}-{j}.pdf pdfs/{conf}/{year}.{conf_name}-main.{j}.pdf"
            os.system(command)

            with open(f"pdfs/{conf}/{year}.{conf_name}-main.{j}.pdf", "rb") as f:
                pdf = pdftotext.PDF(f)

            with open(f"text/{conf}/{year}.{conf_name}-main.{j}.txt", "w") as op:
                op.write("\n\n".join(pdf))
        except:
            pass


for conf, num in zip(conferences_s[1:], short_papers[1:]):
    year = conf[-4:]
    year2 = year[-2:]
    conf_name = conf[:-4]

    if conf_name == "acl":
        conf_id = "P"
    elif conf_name == "emnlp":
        conf_id = "D"
    elif conf_name == "naacl":
        conf_id = "N"

    try:
        os.mkdir(f"text/{conf}")
        os.mkdir(f"pdfs/{conf}")
    except:
        pass
    print(conf, conf_name)
    print(year, year2)
    for i in range(1, num + 1):
        try:
            print(i)
            j = 2000 + i
            command = f"wget https://www.aclweb.org/anthology/{conf_id}{year2}-{j}.pdf"
            os.system(command)
            command = f"mv {conf_id}{year2}-{j}.pdf pdfs/{conf}/{year}.{conf_name}-main.{j}.pdf"
            os.system(command)

            with open(f"pdfs/{conf}/{year}.{conf_name}-main.{j}.pdf", "rb") as f:
                pdf = pdftotext.PDF(f)

            with open(f"text/{conf}/{year}.{conf_name}-main.{j}.txt", "w") as op:
                op.write("\n\n".join(pdf))
        except:
            pass
