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



hanzi = '人';
url = 'http://www.yellowbridge.com/chinese/sentsearch.php?word=' + hanzi;
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

response = requests.get(url, headers=headers);	

soup = BeautifulSoup(response.content, 'html.parser',)	

divs = soup.findAll('span',{'class','zh'});



examples = [];
for div in divs:
	sent = div.get_text("").replace('⑤','').replace('⑩','').replace('{','').replace('}','').replace('⑸','').replace('①','').replace('⑴','').replace('⑴','').replace('⑷','');
	definition = div.find_next("br").get_text("");
	
	examples.append((sent, definition));


