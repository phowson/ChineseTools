# coding=utf-8
import requests
import sys;
from MandarinDefTools import *;
import pinyin;
from gtts import gTTS;
import os;
import csv;

f = open(sys.argv[2], 'w',encoding='utf-8');
ax=0;
with open(sys.argv[1], 'r',encoding='utf-8') as csvfile:
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