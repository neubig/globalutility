

with open("anthology.bib") as inp:
	lines = inp.readlines()

with open('anthology.tsv', 'w') as op:
	op.write(f"ID\tdoi\turl\ttitle\n")
	for l in lines:
		l = l.strip()
		if l[:5] == 'title':
			title = l.split('=')[1].strip()[1:-2]
		elif l[:3] == 'url':
			url = l.split('=')[1].strip()[1:-2]
			ID = url.split('/')[-1]
		elif l[:3] == 'doi':
			doi = l.split('=')[1].strip()[1:-2]
			if title and url and ID and doi:
				op.write(f"{ID}\t{doi}\t{url}\t{title}\n")
			title = ''
			url = ''
			ID = ''
			doi = ''
