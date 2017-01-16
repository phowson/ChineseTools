# coding=utf-8
from bs4 import BeautifulSoup
import requests
import sys;
from sets import Set
from MandarinDefTools import *;
import pinyin;

reload(sys)  
sys.setdefaultencoding('utf8')


numberCharactersVocab=500;

characters = getMostCommonChars(numberCharactersVocab);



response = requests.get('https://en.wiktionary.org/wiki/Appendix:Mandarin_Frequency_lists/1-1000');
html_doc=response.content;


outputFiles=[];
for i in range(0,10):
	f = open('Words unit '+str(i) +'.tsv', 'w');
	outputFiles.append(f);




soup = BeautifulSoup(html_doc, 'html.parser',)

row =  soup.li;

seen=Set();

count = 0;
while row!=None:

	col1=row.find_next("a");
	col2=col1.find_next("a");




	if (col2.get_text("",strip=True)=="Contributions"):
		break;

	char = clean(h.unescape(col2.get_text(" ",strip=True)));
	desc = reduceLen(re.sub('^.*\\(','',clean(h.unescape(row.get_text(" ",strip=True)))));
	row = row.find_next("li");

	# Python is shit.
	if (char in seen):
		continue
	
	seen.add(char);


	ok = True;
	for c in char:
		if (c not in characters):
			ok = False;
			break;

	if not ok:
		print "rejected";
		continue;
	

	line = char;
	line += '\t';
	line += pinyin.get(char);
	line += '<br/>';
	line += re.sub(',',', ',desc).encode('utf-8');
	line += '<br/>';
	line += reduceLen(getDefinition(char));
	line+= '<br/>';
	line += getExamples(char.encode('utf-8'));
	line+= '<br/>';
	line+= 'Rank ' + str(count+1);
	line += '\n';

	f = outputFiles[count/100];
	f.write(line);
	f.flush();
		
	print count;
	count = count+1;

for i in range(0,10):
	outputFiles[i].close();
	
