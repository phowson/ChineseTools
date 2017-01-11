
from bs4 import BeautifulSoup
import requests
import sys;
from sets import Set
from MandarinDefTools import *;

reload(sys)  
sys.setdefaultencoding('utf8')


response = requests.get('http://www.zein.se/patrick/3000char.html');
html_doc=response.content;
html_doc=re.sub('<FONT SIZE=\\+2>','',html_doc);
html_doc=re.sub('<FONT>','',html_doc);
html_doc=re.sub('</FONT>','',html_doc);


soup = BeautifulSoup(html_doc, 'html.parser',)

first_table = soup.table;
second_table = first_table.find_next("table");


outputFiles=[];
for i in range(0,29):
	f = open('Characters unit '+str(i) +' with examples.tsv', 'w');
	outputFiles.append(f);


row = second_table.find_next("tr");
row = row.find_next("tr");

counter = 0;
while row!=None:

	col1=row.find_next("td");
	col2=col1.find_next("td");
	col3=col2.find_next("td");

	char = clean(h.unescape(col2.get_text(" ",strip=True))).encode('utf-8');

	txt = '<font size="2">'+char+'</font>';
	txt+= '\t';
	txt+= reduceLen(clean(h.unescape(col3.get_text(" ",strip=True)))).encode('utf-8');
	txt+= '<br/>';
	txt+= getDefinition(char);
	txt+= '<br/>';
	txt+= getExamples(char);
	txt+= '<br/>';
	txt+= 'Rank ' + str(counter+1);
	txt+= '\n';

	ofls = outputFiles[counter/100];
	ofls.write(txt);
	ofls.flush();

	counter = counter+1;
	print counter;


	row = row.find_next("tr");


for i in range(0,29):
	
	outputFiles[i].close();
