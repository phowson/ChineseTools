
import requests
from MandarinDefTools import *;
import sys;
from gtts import gTTS;
import urllib;



reload(sys)  
sys.setdefaultencoding('utf8')


response = requests.get('http://data.hskhsk.com/lists/HSK%20Official%20With%20Definitions%202012%20L4%20freqorder.txt');

lines = response.content.split('\n');
wordMap = getWordMap();


outputFiles=[];
outputFolderNames=[];

dirPrefix='HSK4Deck';

for i in range(0,13):
	directory = dirPrefix + str(i);
	if not os.path.exists(directory):
		os.makedirs(directory)

	f = open(directory+'/deck.tsv', 'w');
	outputFiles.append(f);
	outputFolderNames.append(directory);


counter = 0;
for row in lines:
	cols = row.split('\t');
	



	if (len(cols)<4):
		break;
	col1=cols[0];
	col2=cols[1];
	col4=cols[3];
	col5=cols[4];



	char = col1.strip();

	x = counter/50;

	sDir = outputFolderNames[x];
	knownWord = wordMap.get(char);
	filename= str(counter) +'.mp3';
	if (os.path.isfile(sDir+'/'+filename)):
		os.remove(sDir+'/'+filename);


	if knownWord is None:
		tts = gTTS(text=char, lang='zh-cn')

		tts.save(sDir+'/'+filename)		
	else:
		print "download "  +knownWord[3]
		urllib.urlretrieve (knownWord[3], sDir+'/'+filename)





	txt= '<font size=+3>';
	txt+= char;
	txt+= '</font>\t';
	txt+= reduceLen(clean(col4));
	txt+= '<br/>';
	txt+= reduceLen(clean(col5));
	txt+= '<br/>';
	txt+= getDefinition(char);
	txt+= '<br/>';
	txt+= getExamples(char);
	txt+= '<br/>';
	txt+= 'Rank ' + str(counter+1);

	tag = "SECTION" + str(counter / 10);

	txt+= '\t'+tag+'\t\t\t'+filename+'\t\n'


	ofls = outputFiles[x];
	ofls.write(txt);
	ofls.flush();





	counter = counter+1;
	print counter;




for f in outputFiles:	
	f.close();


print "compressing"
i=0;
for d in outputFolderNames:
	with zipfile.ZipFile('HSK4 Read deck' + str(i)+'.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
		zipdir(d, zipf);

		i=i+1