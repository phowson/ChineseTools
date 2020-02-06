# coding=utf-8
import requests
import sys;
from sets import Set
from MandarinDefTools import *;
import pinyin as py;
from gtts import gTTS;
import os;
import csv;

reload(sys)  
sys.setdefaultencoding('utf8')
sDir = sys.argv[2] +'/';

sDir1 = sDir +'/MandEng/';
sDir2 = sDir +'/EngMand/';

includeMP3 = False

outputFolderNames=[];

outputFolderNames.append(sDir1)
outputFolderNames.append(sDir2)

for d in outputFolderNames:
	if not os.path.exists(d):
		os.makedirs(d)

ax=0;
f = open(sDir1+'/deck.tsv', 'w');
f2 = open(sDir2 +'/deck.tsv', 'w');
with open(sys.argv[1], 'rb') as csvfile:
	creader = csv.reader(csvfile, delimiter='\t')

	for row in creader:
		if row[0].startswith('//'):
			continue;

		mandarin = row[0];

		if len(row)>=3:
			pinyin = row[1];
			definition = row[2];
		else:
			pinyin = py.get(mandarin)
			definition = getDefinition(mandarin);
		tag = "SECTION" + str(ax/10);


		if includeMP3:
			tts = gTTS(text=mandarin, lang='zh-cn')
			filename = 'sentaudio' + str(ax) +'.mp3';
			if (os.path.isfile(sDir1+filename)):
				os.remove(sDir1+filename);

			if (os.path.isfile(sDir2+filename)):
				os.remove(sDir2+filename);

			tts.save(sDir1+filename);
			tts.save(sDir2+filename);
		else:
			filename = '';

		f.write(mandarin +'\t' + pinyin+ '<br/><p>' + definition +'</p>\t'+tag+'\t\t\t'+filename+'\t\n');
		f.flush();

		f2.write(definition +'\t' + pinyin+ '<br/><p>' + mandarin +'</p>\t'+tag+'\t\t\t\t'+filename+'\n');
		f2.flush();

		ax=ax+1;
		print(str(ax));

f.close();
f2.close();


print "compressing"
i=0;
for d in outputFolderNames:
	with zipfile.ZipFile(sys.argv[2] +"_"+ str(i)+'.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
		zipdir(d, zipf);
		i=i+1