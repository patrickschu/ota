import re
import os
import codecs

#setting up some helper functions
def tagextractor(text, tag, fili):
    regexstring="<"+tag+"=(.*?)>"
    result=re.findall(regexstring, text, re.DOTALL)
    if len(result) != 1:
        print "alarm in tagextractor", fili, result
    return result[0]
    
def adtextextractor(text, fili):
    regexstring="<text>(.*?)</text>"
    result=re.findall(regexstring, text, re.DOTALL)
    if len(result) != 1:
        print "alarm in adtextextractor", fili, result
    return result[0]
    

inputdir="~/Downloads"
inputdir=os.path.expanduser(inputdir)

outputfile=codecs.open(os.path.join(inputdir, "catout.txt"), "a")

for fili in [f for f in os.listdir(os.path.join(inputdir, "ota_0409")) if not f.startswith(".")]:
	inputi=codecs.open(os.path.join(inputdir, "ota_0409", fili), "r")
	inputfile=inputi.read()
	number=tagextractor(inputfile, "no", fili)
	title=tagextractor(inputfile, "otatitle", fili)
	author=tagextractor(inputfile, "author", fili)
	author2=tagextractor(inputfile, "otaauthor", fili)
	genre=tagextractor(inputfile, "genre1", fili)
	print "\n", number, title, author, author2, "\n"
	
	category=raw_input("A(merican) or B(ritish) or O(ther) or U(nknown)?")
	print category
	outputfile.write(",".join([number, title, category])+"\n")
	inputi.close()

outputfile.close()
		