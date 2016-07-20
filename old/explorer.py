import os
import re
import codecs

#setting up some helper functions
def tagextractor(text, tag, fili):
    regexstring="<"+tag+"=(.*?)>"
    result=re.findall(regexstring, text, re.DOTALL)
    if len(result) != 1:
        print "alarm in tagextractor", fili, result
    return result[0]



def explorer(filelist, inputdir, outputlist=False):
	inputdir=os.path.expanduser(inputdir)
	filelist=open(filelist, "r")
	for line in filelist:
		filename=line.rstrip("\n")+".txt"
		inputtext=codecs.open(os.path.join(inputdir, filename)).read()
		dialect=tagextractor(inputtext, "dialect", filename)
		if dialect != "A" and dialect !="U" and dialect !="C":
			print filename, dialect
			if outputlist:
				output=codecs.open("/Users/ps22344/Downloads/goodfiles_0620_16.txt", "a")
				output.write(filename+"\n")
	if outputlist:
		output.close()
	print "finished"
			

explorer('/Users/ps22344/Downloads/ota-master/goodfiles_68.txt', '~/Desktop/ota_0621', True)

	
	