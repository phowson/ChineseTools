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


numberCharactersVocab = 500;
sentPages = 3;
skip = 0;


response = requests.get('http://www.zein.se/patrick/3000char.html');
html_doc=response.content;
html_doc=re.sub('<FONT SIZE=\\+2>','',html_doc);
html_doc=re.sub('<FONT>','',html_doc);
html_doc=re.sub('</FONT>','',html_doc);


soup = BeautifulSoup(html_doc, 'html.parser',)

first_table = soup.table;
second_table = first_table.find_next("table");

sDir = 'sentDeck' + str(numberCharactersVocab) +'/';
f = open(sDir +'deck.tsv', 'w');


row = second_table.find_next("tr");
row = row.find_next("tr");

counter = 0;
characters = list();
permissableInSentences = set();

while row!=None:

	col1=row.find_next("td");
	col2=col1.find_next("td");
	col3=col2.find_next("td");

	char = simplify(clean(h.unescape(col2.get_text(" ",strip=True))));
	characters.append(char);

	row = row.find_next("tr");

	if (len(characters)<numberCharactersVocab):
		permissableInSentences.add(char);
	
permissableInSentences.add(u'！');
permissableInSentences.add(u'。');
permissableInSentences.add(u'？');
permissableInSentences.add(u'，');
permissableInSentences.add(u' ');
permissableInSentences.add(u'您');


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

				#mixer.music.load(filename);
				#mixer.music.play();
				#name = raw_input("Wait") 
				#mixer.music.stop();
				

				print ax;
				ax=ax+1;
			else:
				skip=skip -1;








