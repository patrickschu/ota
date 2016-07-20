import os, codecs,re, math
# print os.getcwd()
# dir="aristotlefiles"
# files=[i for i in os.listdir(dir) if not i.startswith(".")]
# print files
# 
# #for regex
# start="\n----------------------------------------------------------------------\n"
# end="\n----------------------------------------------------------------------\n\nCopyright statement:"
# 
# 
# #for output
# header="<file> <title= > <author=aristotle> <translator= > <source= > <pubdate= > <bibinfo= > <text> "
# footer="</text> </file>"
# 
# for fili in files:
# 	inputfile=codecs.open(os.path.join(dir, fili), "r").read()
# 	regex=re.compile(start+"(.*?)"+end, re.DOTALL)
# 	text=re.findall(regex,inputfile)
# 	output=open("out/"+fili+"_formatted.txt", "w")
# 	output.write(header+text[0]+footer)
# 	output.close()
# 	print fili, "written"
	

	
	# inputtext=adtextextractor(inputfile, fili)
# 			splittext=nltk.word_tokenize(inputtext)
# 			print splittext[:100]

# 
# start="\n----------------------------------------------------------------------\n"
# 
# end="\n----------------------------------------------------------------------\n\nCopyright statement:"
# 
# 
# print len(t)
# 	print t[0][:300]
# 	if len(t) ==0:
# 		print "start", fili
# 		print inputfile[:300]
# 		print "end", fili
# 		print inputfile[len(inputfile)-500: len(inputfile)]

print math.ceil(float(1)/4)
