import codecs 
import re 
import time 
import os 
import nltk 
import string
from string import punctuation

#setting up the output file
outputfile="output.csv"


#reading in the yestlist, nolist or whatever. these are the words to iterate over/search for
yeslist=[]
f=open("/Users/ps22344/Downloads/ota-master/yeslist_regex_620_16.txt", "r")
for line in f:
	yeslist.append(line.rstrip("\n").split("\t"))
	
f.close()

#this is the list with the files/books we're using
goodfiles=[]
f=open("goodfiles_68.txt", "r")

for line in f:
	goodfiles.append(line.rstrip("\n"))

f.close()

# some helper funcs

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

#CAREFUL!! THIS VARIES DEP ON WHERE THE FILE WSS OUTPUT
#
yeslist_words=[i[0] for i in yeslist[1:len(yeslist)]]
print yeslist_words

dicti={i:0 for i in yeslist_words}





output0=codecs.open(outputfile, "a", "utf-8")

#output column names
cols=['uniq', 'filenumber', 'otanumber', 'pubdate', 'genre', 'title', 'wordcount']
output0.write("\t".join(cols)+"\t")
output0.write("\t".join(yeslist_words)+"\n")
output0.close()
#the actual reader
for item in goodfiles:
	try:
		#we open the corpus fils&read it
		#/Users/ps22344/Downloads
		output1=codecs.open(outputfile, "a", "utf-8")
		finput=codecs.open(os.path.join("/Users","ps22344","Downloads", "ota_0409",str(item)+".txt"), "r", "utf-8")
		text=finput.read()
		#we get the metadata
		otanumber=tagextractor(text, "otanumber", item )
		filenumber=tagextractor(text, "no", item )
		pubdate=tagextractor(text, "pubdate", item )
		genre=tagextractor(text, "genre1", item )
		title=tagextractor(text, "otatitle", item )
		content=adtextextractor(text,item)
		contentsplit=nltk.word_tokenize(content)
		print "Before removing punctuation, this text was {} words long".format(len(contentsplit))
		text=[i for i in contentsplit if i not in string.punctuation]
		print "After removing punctuation, this text was {} words long".format(len(text))
		#print len(contentsplit)
		
		#setting up the list for the findings for each text
		results=[]
		#a list of the words well be searching for, to be used in regex
		#write the item from ll, write filenumber etc, add tab for separator
		outputlist=[unicode(item), filenumber, otanumber, pubdate, genre, title, unicode(len(text))]
		output1.write("\t".join(outputlist)+"\t")
		#iterate over all metadata
		output1.close()
		for thing in yeslist_words:
			words=re.findall(r"\b((?:dis|mis|re|un)?"+thing+"\'?)",content)
			dicti[thing]=dicti[thing]+len(words)
			results.append(words)
		print "reading", item, filenumber

		output3=codecs.open(outputfile, "a", "utf-8")
		output3.write("\t".join([str(len(i)) for i in results])+"\n")
		output3.close()
		logout=codecs.open(outputfile+"_log.txt", "a", "utf-8")
		logout.write(str(results)+"\n")
		logout.close()

	except IOError, err:
		print "Error", err
dictiout=open("dicti.txt", "w")
sortdict=sorted(dicti.items(), key=lambda x: x[1], reverse=True)
dictiout.write("\n".join([str(i) for i in sortdict]))
print sortdict
dictiout.close()

#for spreadsheet
for item in yeslist_words:
    print item
    
  