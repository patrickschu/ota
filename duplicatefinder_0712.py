import codecs
import re
from collections import defaultdict

def duplicatefinder(input_file):
	words=[]
	years=[]
	dicti=defaultdict(list)
	with codecs.open(input_file, "r", "utf-8") as inputfile:
		inputi=inputfile.read()
	for lini in inputi.split("\n"):
		words.append(lini.split("\t")[0])
		years.append(lini.split("\t")[1])
		dicti[lini.split("\t")[0]].append(lini)
	
	for key in dicti:
		if len(dicti[key]) != 1:
			print dicti[key], len(dicti[key])
	
	
	
	
	
	
	
duplicatefinder('/Users/ps22344/Downloads/ota-master/paperstuff/gadds_yeslist_withzeros_0713.txt')