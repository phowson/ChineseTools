
hsk5Set = set()


with open('hsk5.txt', 'r', encoding='utf-8') as f:
	lines = f.readlines()	

	for l in lines[1:]:		
		hsk5Set.add(l.strip())


with open('hsksentsfiltered.txt', 'w',  encoding='utf-8') as of:
	with open('hsksents.txt', 'r',  encoding='utf-8') as f:
		lines = f.readlines()

		for l in lines:
			cols = l.split('\t');
			ok = False
			hsk5Words = []
			for w in hsk5Set:
				if w in cols[0]:
					hsk5Words.append(w)
					break;
			if (len(hsk5Words)>0):
				of.write(l.strip() +' HSK5 words='+ str(hsk5Words) +"\n")



