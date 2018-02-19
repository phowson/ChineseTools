# coding=utf-8
import requests
import sys;
from sets import Set
from MandarinDefTools import *;
import pinyin;
from gtts import gTTS;
import os;
import csv;

reload(sys)  
sys.setdefaultencoding('utf8')
lookUpDef = False;



frequencies = {};
with open('frequencyRanking.csv', 'rb') as csvfile:
	creader = csvfile.readlines();

	for row in creader:
		row = unicode(row).strip();
		cols = row.split(',');
		frequencies[cols[0]] = float(cols[1]);

seen = set();

with open(sys.argv[2], 'w') as f:
	ax=0;


	out = [];
	with open(sys.argv[1], 'rb') as csvfile:
		creader = csvfile.readlines();

		for row in creader:
			row = row.strip();
			if row.startswith("//"):
				f.write(row+"\n");

			else:
				mandarin = unicode(row);
				definition = None;
				if lookUpDef:
					definition= getDefinition(mandarin);

				rank =0;
				den = len(mandarin);

				
				for i in range(len(mandarin)):
					c = mandarin[i];

					if frequencies.has_key(c):
						rank =  rank + frequencies[c];

				rank = rank / float(den);
				

				if mandarin not in seen:
						out.append(( rank, mandarin, pinyin.get(mandarin),definition)  );
						seen.add(mandarin);


				ax=ax+1;
				print(str(ax));

	out.sort(reverse=True);

	for rank, mandarin, pys, definition in out:
		print(rank);
		if definition is not None:
			f.write(mandarin +'\t' + pys+ '\t' + definition +'\n');
		else:
			f.write(mandarin + '\n');
	
