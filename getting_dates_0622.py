##extractor
import os
import codecs
import re



input="/Users/ps22344/Desktop/stuff/"

files= [i for i in os.listdir(input) if not i.startswith(".") ]

print files

outputfile="alllist_0623.txt"
output=codecs.open(outputfile, "a")

for fili in files:
	print fili
	inputi=codecs.open(os.path.join(input,fili), "r").read()
	words= inputi.split("\n")[0].split("\t")
	dates= inputi.split("\n")[1].split("\t")
	print "words", len(words)
	print "dates", len(dates)
	diff = len(words) - len(dates)
	print diff
	result=zip(words[:len(words)-diff], dates)
	# print "before", result
 	result=[(i.replace("\xcb\x88",""), re.sub("-\d+", "", j.lstrip(" a?c").rstrip("?"))) for (i,j) in result]
# 	print "after", 
	for t in result:
		print t[0], "\t", t[1]
		output.write(t[0]+"\t"+t[1]+"\n")
	
output.close()
		

