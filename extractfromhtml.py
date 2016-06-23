##extract from html
import os
import re
import codecs
from bs4 import BeautifulSoup
## format words "\n" years


inputfolder="/Users/ps22344/Desktop/html/"

outputfile = "ment1400s_output"

files=[i for i in os.listdir(inputfolder) if not i.startswith(".")]



for fili in files:
	output= codecs.open(outputfile+fili[:3]+".txt", "a", "utf-8")
	html=codecs.open(os.path.join(inputfolder, fili), "r", "utf-8").read()
	soup = BeautifulSoup(html, 'html.parser')
	#print soup
	words = [i.string for i in soup.find_all('span', 'hw') if i.string]
	years = [i.string for i in soup.find_all('span', 'year') if i.string]
	# print words, len(words)
# 	print years, len(years)
	output.write("\t".join(words)+"\n"+"\t".join(years))
	output.close()
	

#Advanced search results _ Oxford English Dictionary.htm



