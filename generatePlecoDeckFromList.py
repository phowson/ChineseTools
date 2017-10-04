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
sys.setdefaultencoding('utf8')
f = open(sys.argv[2], 'w');
ax=0;
with open(sys.argv[1], 'rb') as csvfile:
	creader = csvfile.readlines();

	for row in creader:
		row = row.strip();
		if row.startswith("//"):
			f.write(row+"\n");

		else:
			mandarin = row;
			definition= getDefinition(mandarin);
			f.write(mandarin +'\t' + pinyin.get(mandarin)+ '\t' + definition +'\n');
			ax=ax+1;
			print(str(ax));


		f.flush();


f.close();