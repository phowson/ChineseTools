
import re;
import sys;
import mafan;
from mafan import simplify, tradify;
import requests
from bs4 import BeautifulSoup
from HTMLParser import HTMLParser
h = HTMLParser();



def clean(s):
	return re.sub('>','',re.sub('<','',re.sub('\\r','',re.sub('\\(A.*?\\)','',re.sub('\\(F.*?\\)','',re.sub('\\n','',re.sub('\t',' ', re.sub('&LT;','<',re.sub('&GT;','>',s))))))))).strip();

def reduceLen(s):
	return s[:200];





def getExamplesWithList(char,lst,maxPages):
	for page in range(1,maxPages):
		response = requests.get('http://tatoeba.org/eng/sentences/search/page:'+str(page) +'?query='+char+'&from=cmn&to=eng&orphans=no&unapproved=no&native=yes&user=&tags=&list=&has_audio=&trans_filter=limit&trans_to=eng&trans_link=direct&trans_user=&trans_orphan=no&trans_unapproved=no&trans_has_audio=&sort=words');	

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
	lst = list();
	getExamplesWithList(char,lst,2);
	for t in lst:
		txt+=t[0] +' : ' +t[1] +'<br/>';

	return txt;




def getDefinition(char):
	response = requests.get('https://www.mdbg.net/chindict/chindict.php?wdqb='+char);	
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
