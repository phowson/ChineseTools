# coding=utf-8
from bs4 import BeautifulSoup
import requests
import sys;
from sets import Set
from MandarinDefTools import *;
import pinyin;
from pygame import mixer # Load the required library
from gtts import gTTS;
import os;

mixer.init()
reload(sys)  
sys.setdefaultencoding('utf8')


numberCharactersVocab = 350;
sentPages = 3;
skip = 0;

sDir = 'sentDeck' + str(numberCharactersVocab) +'/';
f = open(sDir +'deck.tsv', 'w');
characters = list();


permissableInSentences = getMostCommonCharsWithList(numberCharactersVocab, characters);


print "Retrieved " + str(len(characters)) +" characters";

alreadySeen = set();
ax = 0;
for c in characters:

	if (c not in permissableInSentences):
		break;

	examplesList = list();
	getExamplesWithList(c, examplesList,sentPages);

	for pair in examplesList:
		mandarin = pair[0];
		definition = pair[1];

		ok = True;
		for cx in mandarin:
			if (cx not in permissableInSentences):
				ok = False;
				break;

		if (ok and mandarin not in alreadySeen):
			alreadySeen.add(mandarin);
			if (skip==0):
				tts = gTTS(text=mandarin, lang='zh-cn')
				filename = 'sentaudio' + str(ax) +'.mp3';
				if (os.path.isfile(sDir+filename)):
					os.remove(sDir+filename);

				tts.save(sDir+filename)
				tag = 'Section' + str(1+ax/100);
				f.write(mandarin +'\t' + pinyin.get(mandarin)+ '<br/><p>' + definition +'</p>\t'+tag+'\t\t\t'+filename+'\t\n');
				f.flush();
				print ax;
				ax=ax+1;
			else:
				skip=skip -1;








