# coding=utf-8
import requests
import sys;
from sets import Set
from MandarinDefTools import *;
import pinyin;
from gtts import gTTS;
import os;
import csv;
import urllib;
import eyed3;

import re
reload(sys)  
sys.setdefaultencoding('utf-8');

textInput = sys.argv[1];
sDir= sys.argv[2] +'/';

if not os.path.isdir(sDir):
	os.makedirs(sDir)


with open(textInput, 'r') as f:
	text = f.read() ;

text = text.decode("utf-8")
sentence='';
ax = 0;
x = re.compile('[\\。]');
for c in text:

	if c=='。':		
		print str(ax);
		tts = gTTS(text=sentence, lang='zh-cn')
		filename = 'speech-' + str(ax) +'.mp3';
		if (os.path.isfile(sDir+filename)):
			os.remove(sDir+filename);

		tts.save(sDir+filename);

		mf = eyed3.load(sDir+filename)
		mf.tag = eyed3.id3.tag.Tag()
		mf.tag.artist =u'Chinese Text To Speech'
		mf.tag.album=sys.argv[2].decode("utf-8");
		mf.tag.title=str(ax).decode("utf-8");
		mf.tag.track_num = ax+1
		mf.tag.save()


		ax = ax+1;
		sentence='';
	else:
		sentence = sentence + c;
		