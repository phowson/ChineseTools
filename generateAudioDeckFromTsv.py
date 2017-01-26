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
sDir = sys.argv[2] +'/';
f = open(sDir +'deck.tsv', 'w');

ax=0;

with open(sys.argv[1], 'rb') as csvfile:
	creader = csv.reader(csvfile, delimiter='\t')

	for row in creader:
		mandarin = row[0];
		definition = row[1];
		tag = "SECTION" + str(ax/10);

		tts = gTTS(text=mandarin, lang='zh-cn')
		filename = 'sentaudio' + str(ax) +'.mp3';
		if (os.path.isfile(sDir+filename)):
			os.remove(sDir+filename);

		tts.save(sDir+filename);
		f.write(mandarin +'\t' + pinyin.get(mandarin)+ '<br/><p>' + definition +'</p>\t'+tag+'\t\t\t'+filename+'\t\n');
		f.flush();
		ax=ax+1;
		print(str(ax));

f.close();