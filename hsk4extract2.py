
import requests
from MandarinDefTools import *;
import sys;
from gtts import gTTS;
import urllib;



reload(sys)  
sys.setdefaultencoding('utf8')



DIVISOR=300;
FOLDERS=2
includeExamples=False;
inlcudeMp3 = False;

response = requests.get('http://data.hskhsk.com/lists/HSK%20Official%20With%20Definitions%202012%20L4%20freqorder.txt');

lines = response.content.split('\n');


outputFiles=[];
outputFilesRev=[];
outputFolderNames=[];
outputFolderNamesRev=[];

dirPrefix='HSK4DeckZhEng';
dirPrefix2='HSK4DeckEngZh';

for i in range(0,FOLDERS):
	directory = dirPrefix + str(i);
	directory2 = dirPrefix2 + str(i);
	

	if not os.path.exists(directory):
		os.makedirs(directory)

	if not os.path.exists(directory2):
		os.makedirs(directory2)

	f = open(directory+'/deck.tsv', 'w');
	outputFiles.append(f);
	outputFolderNames.append(directory);


	f2 = open(directory2+'/deck.tsv', 'w');
	outputFilesRev.append(f2);
	outputFolderNamesRev.append(directory2);


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

	x = counter/DIVISOR;

	sDir = outputFolderNames[x];
	sDir2 = outputFolderNamesRev[x];
	#knownWord = wordMap.get(char);
	if inlcudeMp3:
		filename= str(counter) +'.mp3';
		if (os.path.isfile(sDir+'/'+filename)):
			os.remove(sDir+'/'+filename);
		tts = gTTS(text=char, lang='zh-cn')
		tts.save(sDir+'/'+filename)		
		tts.save(sDir2+'/'+filename)		


	if includeExamples:
		examples = getExamples(char);
	else:
		examples='';

	tag = "SECTION" + str(counter / 10);

	txt= '<font size=+3>';
	txt+= char;
	txt+= '</font>\t';
	txt+= reduceLen(clean(col4));
	txt+= '<br/>';
	txt+= reduceLen(clean(col5));
	txt+= '<br/>';
	txt+= getDefinition(char);
	txt+= '<br/>';
	txt+= examples
	txt+= '<br/>';
	txt+= 'Rank ' + str(counter+1);
	if inlcudeMp3:
		txt+= '\t'+tag+'\t\t\t'+filename+'\t\n'
	else:
		txt+= '\n';


	ofls = outputFiles[x];
	ofls.write(txt);
	ofls.flush();



	txt2= getDefinition(char);	
	txt2+= '<br/>';
	txt2+= reduceLen(clean(col5));
	txt2+= '\t';
	txt2+= char;
	txt2+= '<br/>';
	txt2+= reduceLen(clean(col4));
	txt2+= '<br/>';
	txt2+= examples;
	txt2+= '<br/>';
	txt2+= 'Rank ' + str(counter+1);
	if inlcudeMp3:
		txt2+= '\t'+tag+'\t\t\t'+filename+'\t\n'
	else:
		txt2+= '\n';

	ofls2 = outputFilesRev[x];
	ofls2.write(txt2);
	ofls2.flush();




	counter = counter+1;
	print counter;




for f in outputFiles:	
	f.close();

for f in outputFilesRev:	
	f.close();



if inlcudeMp3:

	print "compressing"
	i=0;

	for d in outputFolderNamesRev:
		with zipfile.ZipFile('HSK4 EngZh deck' + str(i)+'.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
			zipdir(d, zipf);

			i=i+1

	for d in outputFolderNames:
		with zipfile.ZipFile('HSK4 ZhEng deck' + str(i)+'.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
			zipdir(d, zipf);

			i=i+1
