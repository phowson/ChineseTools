
import re;
import sys;
import mafan;
from mafan import simplify, tradify;
import requests
from bs4 import BeautifulSoup
from HTMLParser import HTMLParser
h = HTMLParser();

def clean(s):
	return re.sub('\\r','',re.sub('\\(A.*?\\)','',re.sub('\\(F.*?\\)','',re.sub('\\n','',re.sub('\t',' ', re.sub('&LT;','<',re.sub('&GT;','>',s))))))).strip();

def reduceLen(s):
	return s[:200];


def getExamples(char):

	response = requests.get('http://tatoeba.org/eng/sentences/search?query='+char+'&from=cmn&to=und&orphans=no&unapproved=no&user=&tags=&list=&has_audio=&trans_filter=limit&trans_to=eng&trans_link=direct&trans_user=&trans_orphan=&trans_unapproved=&trans_has_audio=&sort=words');	
	soup = BeautifulSoup(response.content, 'html.parser',)	

	divs = soup.findAll('div',{'class','sentence-and-translations'});

	output='';
	for div in divs:
		sentences = div.findAll('div',{'class','sentence'});
		dt =  div.findAll('div',{'class','direct translations'});
		s=sentences[0];
		translationText = None;

		madarinText= s.find_next('div',{'class','text'}).get_text(" ",strip="true");
		for t in dt:
			trans = t.findAll('div',{'class','translation '});
			for x in trans:
				if x.find_next('div',{'class','lang'}).find_next('img').get('title','')=='English':
					translationText = x.find_next('div',{'class','text'}).get_text(" ",strip="true");
					break;

		if (translationText!=None) :
			output+=simplify(madarinText) + ' : ' + translationText + '<br/>';

	return output;








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
			x = h.unescape(row.get_text(" ",strip=True));
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
