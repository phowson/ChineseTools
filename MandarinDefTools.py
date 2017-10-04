# coding=utf-8

import re;
import sys;
import mafan;
from mafan import simplify, tradify;
import requests
from bs4 import BeautifulSoup
from HTMLParser import HTMLParser
import zipfile
import os;
import time;
import urllib2;
import random;
import cookielib;
from fake_useragent import UserAgent

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file), file)


h = HTMLParser();


def getWordMap():
	words = {};

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
				hanzi = col1.get_text().encode('UTF-8');
				pinYin = col2.get_text();
				translation = col3.get_text();
				hskLevel = col4.get_text();
				words[hanzi] = ( hanzi, pinYin, translation, mp3Path);

				row = row.find_next("tr");
			print len(words);
	return words;




def getMostCommonChars(numberCharactersVocab): 
	return getMostCommonCharsWithList(numberCharactersVocab, list());


def getMostCommonCharsWithList(numberCharactersVocab, characters):
	response = requests.get('http://www.zein.se/patrick/3000char.html');
	html_doc=response.content;
	html_doc=re.sub('<FONT SIZE=\\+2>','',html_doc);
	html_doc=re.sub('<FONT>','',html_doc);
	html_doc=re.sub('</FONT>','',html_doc);


	soup = BeautifulSoup(html_doc, 'html.parser',)

	first_table = soup.table;
	second_table = first_table.find_next("table");




	row = second_table.find_next("tr");
	row = row.find_next("tr");

	counter = 0;
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
	permissableInSentences.add(u'谢');
	permissableInSentences.add(u'啊');
	permissableInSentences.add(u'她');
	permissableInSentences.add(u'他');
	permissableInSentences.add(u'它');
	permissableInSentences.add(u'那');
	permissableInSentences.add(u'这');
	permissableInSentences.add(u'哪');
	permissableInSentences.add(u'人');
	permissableInSentences.add(u'不');
	permissableInSentences.add(u'的');
	permissableInSentences.add(u'子');
	permissableInSentences.add(u'得');
	permissableInSentences.add(u'地');
	permissableInSentences.add(u'一');
	permissableInSentences.add(u'二');
	permissableInSentences.add(u'三');
	permissableInSentences.add(u'四');
	permissableInSentences.add(u'五');
	permissableInSentences.add(u'六');
	permissableInSentences.add(u'七');
	permissableInSentences.add(u'八');
	permissableInSentences.add(u'九');
	permissableInSentences.add(u'两');
	permissableInSentences.add(u'个');
	permissableInSentences.add(u'十');
	permissableInSentences.add(u'零');

	permissableInSentences.add(u'了');
	permissableInSentences.add(u'？');
	permissableInSentences.add(u'“');
	permissableInSentences.add(u'”');
	permissableInSentences.add(u'!');
	permissableInSentences.add(u'.');
	permissableInSentences.add(u',');
	return permissableInSentences;


def clean(s):
	return re.sub('>','',re.sub('<','',re.sub('\\r','',re.sub('\\(A.*?\\)','',re.sub('\\(F.*?\\)','',re.sub('\\n','',re.sub('\t',' ', re.sub('&LT;','<',re.sub('&GT;','>',s))))))))).strip();

def reduceLen(s):
	return s[:200];


def getExamplesListFromYellowBridge(hanzi):
	ua = UserAgent()
	url = 'http://www.yellowbridge.com/chinese/sentsearch.php?word=' + hanzi;
	headers = {'User-Agent': ua.random, 
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
	'Accept-Language':'en-GB,en;q=0.5',
	'Accept-Encoding':'gzip, deflate'

	};

	sessionId = str(round(random.random()*10000000));
	cookies = dict(
	cookies_are='working', 
	PHPSESSID=sessionId,
	_ga='GA1.2.108927118.1479826512',
	_gat='1');

	print "Sleep for a bit"
	time.sleep(random.random()*10+3)
	print "Slept, now spam yellowbridge " +url



	response = requests.get(url, headers=headers, cookies=cookies);	

	soup = BeautifulSoup(response.content, 'html.parser',)	
	divs = soup.findAll('span',{'class','zh'});



	examples = [];
	for div in divs:
		sent = div.get_text("").replace('④','').replace('⑤','').replace('⑩','').replace('{','').replace('}','').replace('⑸','').replace('①','').replace('⑴','').replace('⑴','').replace('⑷','').replace('⑵','').replace('③','').replace('。','').replace('②','').replace('⑶','').strip();
		definition = div.find_next("br").get_text("");
		
		examples.append((simplify(clean(h.unescape(sent))), definition));

	return examples;




def getExamplesWithList(char,lst,maxPages):
	for page in range(1,maxPages):
		url = 'http://tatoeba.org/eng/sentences/search/page:'+str(page) +'?query='+char+'&from=cmn&to=eng&orphans=no&unapproved=no&native=yes&user=&tags=&list=&has_audio=&trans_filter=limit&trans_to=eng&trans_link=direct&trans_user=&trans_orphan=no&trans_unapproved=no&trans_has_audio=&sort=words';
		response = requests.get(url);	

		soup = BeautifulSoup(response.content, 'html.parser',)	

		divs = soup.findAll('div',{'class','sentence-and-translations'});

		for div in divs:
			sentences = div.findAll('div',{'class','sentence'});
			dt =  div.findAll('div',{'class','direct translations'});
			s=sentences[0];
			translationText = None;

			mandarinText= simplify(s.find_next('div',{'class','text'}).get_text(" ",strip="true")).strip();
			for t in dt:
				trans = t.findAll('div',{'class','translation '});
				for x in trans:
					if x.find_next('div',{'class','lang'}).find_next('img').get('title','')=='English':
						translationText = x.find_next('div',{'class','text'}).get_text(" ",strip="true");
						break;

			if (translationText!=None) :
				lst.append((mandarinText, translationText));



def getExamples(char):
	txt='';
	lst0 = getExamplesListFromYellowBridge(char);
	lst = list();
	getExamplesWithList(char,lst,2);


	for t in lst0:
		txt+=t[0] +' : ' +t[1] +'<br/>';

	for t in lst:
		txt+=t[0] +' : ' +t[1] +'<br/>';

	return txt;




def getDefinition(char):

	success = False;

	while not success:

		try:
			response = requests.get('https://www.mdbg.net/chindict/chindict.php?wdqb='+char);	
			success=True
		except Exception:
			success=False
			print "Retry definition service"

	soup = BeautifulSoup(response.content, 'html.parser',)	

	tables = soup.findAll('table',{'class','wordresults'});
	
	row1= tables[0].find_next("tr");
	row= row1.find_next("tr");


	col1 = row.find_next('td');

	first = None;
	HSK = None;
	while col1!=None:

		utf1 = col1.get_text();
		if (char in utf1):

			dv = row.find_next("div",{'class','defs'});

			x = h.unescape(dv.get_text(" ",strip=True));
			if ("surname" not in x and "Surname" not in x and "variant of" not in x and "Variant of" not in x):				
				if (first==None):
					first = x;
				if ('HSK' in x and HSK == None):
					HSK = x;

	


		row = row.find_next('tr');		
		if (row==None):
			break;
		col1 = row.find_next('td');		

	if (HSK!=None):
		return HSK;
	if (first!=None):
		return first;

	return "None on MDBG";
