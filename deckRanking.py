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




frequencies = {};
with open('frequencyRanking.csv', 'rb') as csvfile:
	creader = csvfile.readlines();

	for row in creader:
		row = unicode(row).strip();
		cols = row.split(',');
		frequencies[cols[0]] = float(cols[1]);


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
				definition= getDefinition(mandarin);

				rank =0;
				den = len(mandarin);

				print(mandarin);
				for i in range(len(mandarin)):
					c = mandarin[i];
					print(c);

					if frequencies.has_key(c):
						rank =  rank + frequencies[c];

				rank = rank / float(den);
				print(rank);
				out.append(( rank, mandarin, pinyin.get(mandarin),definition)  );


				ax=ax+1;
				print(str(ax));

	out.sort(reverse=True);

	for mandarin, pys, definition in out:
		f.write(mandarin +'\t' + pys+ '\t' + definition +'\n');
	
