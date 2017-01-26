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
sys.setdefaultencoding('utf8');

characters = list();
getMostCommonCharsWithList(3000, characters);

words = list();

for i in range(1,6):
	print i;
	with open('WordLists\\' + str(i) +'.html', 'r') as f:
		html_doc= f.read();
		soup = BeautifulSoup(html_doc, 'html.parser',)
		first_table = soup.table;
		row = first_table.find_next("tr");
		while (row!=None):
			col1 = row.find_next("td", {"class", "s4"});
			col2 = col1.find_next("td", {"class", "s4"});
			if (col2==None):
				break;
			col3 = col2.find_next("td", {"class", "s5"});
			col3 = col3.find_next("td", {"class", "s5"});
			col4 = col3.find_next("td", {"class", "s3"});
			col5 = col4.find_next("td", {"class", "s7"});

			mp3Path = col5.a['href'];


			hanzi = col1.get_text();
			pinYin = col2.get_text();
			translation = col3.get_text();
			hskLevel = col4.get_text();


			rank = int(hskLevel)*1000;
			for c in  hanzi:
				try:
					rank += characters.index(c);
					break;
				except ValueError:
					rank += 3000;


			words.append((rank, hanzi, pinYin, translation, mp3Path));

			row = row.find_next("tr");
		print len(words);



words = sorted(words);
deckSize = 50;
requiredDirectories = len(words) / deckSize;



