
import requests
from MandarinDefTools import *;
import sys;

reload(sys)  
sys.setdefaultencoding('utf8')


response = requests.get('http://data.hskhsk.com/lists/HSK%20Official%20With%20Definitions%202012%20L4%20freqorder.txt');

lines = response.content.split('\n');


outputFiles=[];
for i in range(0,13):
	f = open('HSK unit '+str(i) +' with examples.tsv', 'w');
	outputFiles.append(f);



counter = 0;
for row in lines:
	cols = row.split('\t');
	if (len(cols)<4):
		break;
	col1=cols[0];
	col2=cols[1];
	col4=cols[3];
	col5=cols[4];



	char = col1;



	txt= '<h1>';
	txt+= char;
	txt+= '</h1>\t';
	txt+= reduceLen(clean(col4));
	txt+= '<br/>';
	txt+= reduceLen(clean(col5));
	txt+= '<br/>';
	txt+= getDefinition(char);
	txt+= '<br/>';
	txt+= getExamples(char);
	txt+= '<br/>';
	txt+= 'Rank ' + str(counter+1);
	txt+= '\n';

	ofls = outputFiles[counter/50];
	ofls.write(txt);
	ofls.flush();

	counter = counter+1;
	print counter;




for f in outputFiles:	
	f.close();
