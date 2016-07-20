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
    
def labeladder(inputdir, outputfile, *args):
	"""
	This takes files from an inputdir, lets the user add labels and then write their input to the outputfile.
	Takes any number of pre-existing labels as arguments 
	"""
	
	inputdir=inputdir
	inputdir=os.path.expanduser(inputdir)
	outputfile=codecs.open(os.path.join(inputdir, outputfile), "a")

	for fili in [f for f in os.listdir(os.path.join(inputdir)) if not f.startswith(".")]:
		inputi=codecs.open(os.path.join(inputdir, fili), "r")
		inputfile=inputi.read()
		data_to_display=[]
		for arg in args:
			data_to_display.append(tagextractor(inputfile, "no", fili))
		print ", ".join([str(d) for d in data_to_display])	
		
		category=raw_input("A(merican) or B(ritish) or O(ther) or U(nknown)?\n")
		print category
		outputfile.write(",".join([str(d) for d in data_to_display])+","+category+"\n")
		inputi.close()

	outputfile.close()
		