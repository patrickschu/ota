##ADDING METADATA


import os
import codecs
import re




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
    

	



def metadatabuilder(labelfile, inputfolder, outputfolder):
	"""
	labelfile needs to be comma separated, with file ID the first and new label the last element of each row.
	"""
		
	inputdir=inputfolder
	inputdir=os.path.expanduser(inputdir)
	
	outputdir=outputfolder
	outputdir=os.path.expanduser(outputdir)
	
	for line in codecs.open(labelfile, "r"):
		splitline=line.split(",")
		file_id=splitline[0]
		if int(file_id) > 1228 and int(file_id) <1349:
			new_label=splitline[len(splitline)-1].rstrip("\n")
			print os.path.join(inputfolder, file_id+".txt")
			inputfile=codecs.open(os.path.join(inputdir, file_id+".txt")).read()
			number=tagextractor(inputfile, "no", file_id)
			print file_id, number, new_label
			outputfile=re.sub("> <authorage=", "> <dialect="+new_label.rstrip(" ")+"> <authorage=", inputfile)
			output=codecs.open(os.path.join(outputdir, file_id+".txt"), "w")
			output.write(outputfile)
			output.close()		
		

	
	
metadatabuilder('/Users/ps22344/Downloads/ota-master/catout_corrected.txt', '~/Downloads/ota_0409', '~/Desktop/ota_0621')
	