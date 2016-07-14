# -*- coding: utf-8 -*-



import codecs 
import re 
import time 
import os 
import nltk 
import string
from string import punctuation
import pandas
import re
import json
import codecs
from collections import defaultdict
import os

now=time.time()


yeslist=[]
f=codecs.open("/Users/ps22344/Downloads/ota-master/paperstuff/alllist_0712_corrected_regex.txt_pandas_0to1700.txt", "r", "utf-8")
for line in f:
	yeslist.append(line.rstrip("\n").split("\t"))
	
f.close()

#WATCH THIS SETTING
yeslist_words=[i[1] for i in yeslist]
print "yeslist", yeslist_words





inputi=pandas.read_csv('/Users/ps22344/Downloads/ota-master/paperstuff/output_alllist_0713', sep="\t")


def periodfinder(inputspread, start_time, interval):
	"""
	The periodfinder extracts all data points from inputspread that satisfy the criteria
	'larger than or equal to start_time' and 'smaller than start_time + interval'.
	Returns a spreadsheet.
	"""	
	print "Running periodfinder for {} - {}".format(start_time,start_time+interval -1)
	outputspread=inputspread.loc[(inputspread['pubdate']>=start_time) & (inputspread['pubdate']<start_time+interval)]
	return outputspread


def adtextextractor(text, fili):
    regexstring="<text>(.*?)</text>"
    result=re.findall(regexstring, text, re.DOTALL)
    if len(result) != 1:
        print "alarm in adtextextractor", fili, result
    return result[0]

def dictwriter(file_name, dictionary, sort_dict=True):
	"""
	writes out a dictionary to a text file after sorting it
	"""
	print "Starting the dictionarywriter, sorting is", sort_dict
	sorteddict=sorted(dictionary.items(), key=lambda x: x[1], reverse=True)
	with codecs.open(file_name, "w", "utf-8") as outputi:
		outputi.write("\n".join([str(i) for i in sorteddict]))
	with open(file_name+".json", "w") as jsonoutputi:
		json.dump(dictionary, jsonoutputi,  encoding="utf-8")
	
header="\n\n-------\n"
	

def main(inputspread, start_time, end_time, interval):
	"""
	Creates periods between start_time and end_time as determined by interval. 
	For each, relevant texts are extracted and words are counted. 
	In the end, full dictionary and hapax dictionary are output as txt file and json.
	"""
	overalldicti=defaultdict(dict)
	spreadsheet=pandas.DataFrame()
	for item in range(start_time, end_time, interval):
		print header, item, header
		subsetspread= periodfinder(inputspread, item, interval) 
		perioddicti=defaultdict(list)
		#iterating over all the files contained in the extracted spreadsheet
		for fileno in subsetspread['filenumber']:
			#read file
			with codecs.open(os.path.join('/Users/ps22344/Downloads/ota_0621', unicode(fileno)+".txt"), "r", "utf-8") as inputfili:
				inputtext=inputfili.read()
			content=adtextextractor(inputtext,item)
			contentsplit=nltk.word_tokenize(content)
			#print "Before removing punctuation, this text was {} words long".format(len(contentsplit))
			text=[i.lower() for i in contentsplit if not re.match(r"\d+", i)]
			text= [re.sub(r"('s|s|s's|ed)\b", "", i) for i in text if i not in string.punctuation]
			#print "After removing punctuation, this text was {} words long".format(len(text))
			for word in text:
				perioddicti[word].append(word)
		print header, "Number of words in perioddicti is", len(perioddicti)
		hapaxdicti= {k:v for k,v in perioddicti.items() if v == 1}
		dictwriter(unicode(item)+"to"+unicode(item+interval-1)+"hapax_dict.txt", hapaxdicti)
		dictwriter(unicode(item)+"to"+unicode(item+interval-1)+"_dict.txt", perioddicti)
		for entry in perioddicti:
			overalldicti[entry][item]=len(perioddicti[entry])
	
	print "Writing the overalldicti to file"
	dictwriter(unicode(start_time)+"to"+unicode(end_time)+"overall_dict.txt", overalldicti)
	
	print "Making hapaxdicti"	
	overallhapax={k:v for k,v in overalldicti.items() if sum(v.values()) == 1}
	print "Overall hapax has {} entries".format(len(overallhapax))
	print "Write to file"
	dictwriter(unicode(start_time)+"to"+unicode(end_time)+"overall_hapaxdict.txt", overallhapax)



main(inputi, 1700, 1800, 10)























# #setting up the output file
# outputfile="output_gaddlist_0714"
# print outputfile
# 
# #reading in the yeslist, nolist or whatever. these are the words to iterate over/search for
# yeslist=[]
# f=codecs.open("/Users/ps22344/Downloads/ota-master/paperstuff/gadds_yeslist_withzeros_0713.txt_pandas_0to1700.txt", "r", "utf-8")
# for line in f:
# 	yeslist.append(line.rstrip("\n").split("\t"))
# 	
# f.close()
# 
# #WATCH THIS SETTING
# yeslist_words=[i[1] for i in yeslist]
# 
# print yeslist_words, "\n"
# print "we have {} words\n".format(len(yeslist_words))
# #this is the list with the files/books we're using
# goodfiles=[]
# f=open("/Users/ps22344/Downloads/ota-master/paperstuff/goodfiles_0620_16.txt", "r")
# 
# for line in f:
# 	goodfiles.append(line.rstrip("\n"))
# 
# f.close()
# print "we have {} files\n".format(len(goodfiles))
# # some helper funcs
# 
# def tagextractor(text, tag, fili):
#     regexstring="<"+tag+"=(.*?)>"
#     result=re.findall(regexstring, text, re.DOTALL)
#     if len(result) != 1:
#         print "alarm in tagextractor", fili, result
#     return result[0]
# 
# def adtextextractor(text, fili):
#     regexstring="<text>(.*?)</text>"
#     result=re.findall(regexstring, text, re.DOTALL)
#     if len(result) != 1:
#         print "alarm in adtextextractor", fili, result
#     return result[0]
# 
# #CAREFUL!! THIS VARIES DEP ON WHERE THE FILE WSS OUTPUT
# #
# 
# 
# dicti={i:0 for i in yeslist_words}
# 
# for period in range(1700, 1800, 10):
# 	print period
# 
# 
# 
# output0=codecs.open(outputfile, "a", "utf-8")
# 
# #output column names
# cols=['uniq', 'filenumber', 'otanumber', 'pubdate', 'genre', 'title', 'wordcount']
# output0.write("\t".join(cols)+"\t")
# output0.write("\t".join(yeslist_words)+"\n")
# output0.close()
# #the actual reader
# for item in goodfiles:
# 	try:
# 		#we open the corpus fils&read it
# 		#/Users/ps22344/Downloads
# 		output1=codecs.open(outputfile, "a", "utf-8")
# 		finput=codecs.open(os.path.join("/Users","ps22344","Downloads", "ota_0621",str(item)+".txt"), "r", "utf-8")
# 		text=finput.read()
# 		#we get the metadata
# 		otanumber=tagextractor(text, "otanumber", item )
# 		filenumber=tagextractor(text, "no", item )
# 		pubdate=tagextractor(text, "pubdate", item )
# 		genre=tagextractor(text, "genre1", item )
# 		title=tagextractor(text, "otatitle", item )
# 		content=adtextextractor(text,item)
# 		contentsplit=nltk.word_tokenize(content)
# 		print "Before removing punctuation, this text was {} words long".format(len(contentsplit))
# 		text=[i for i in contentsplit if i not in string.punctuation]
# 		print "After removing punctuation, this text was {} words long".format(len(text))
# 		#print len(contentsplit)
# 		
# 		#setting up the list for the findings for each text
# 		results=[]
# 		#a list of the words well be searching for, to be used in regex
# 		#write the item from ll, write filenumber etc, add tab for separator
# 		outputlist=[unicode(item), filenumber, otanumber, pubdate, genre, title, unicode(len(text))]
# 		output1.write("\t".join(outputlist)+"\t")
# 		#iterate over all metadata
# 		output1.close()
# 		for thing in yeslist_words:
# 			#no suffix
# 			words=re.findall(r"\b("+thing+"\'?)",content)
# 			#yes suffix
# 			#words=re.findall(r"\b((?:dis|mis|re|un)?"+thing+"\'?)",content)
# 			dicti[thing]=dicti[thing]+len(words)
# 			results.append(words)
# 		print "reading", item, filenumber
# 
# 		output3=codecs.open(outputfile, "a", "utf-8")
# 		output3.write("\t".join([str(len(i)) for i in results])+"\n")
# 		output3.close()
# 		logout=codecs.open(outputfile+"_log.txt", "a", "utf-8")
# 		logout.write(str(results)+"\n")
# 		logout.close()
# 
# 	except IOError, err:
# 		print "Error", err
# dictiout=open(outputfile+"_dicti.txt", "w")
# sortdict=sorted(dicti.items(), key=lambda x: x[1], reverse=True)
# dictiout.write("\n".join([str(i) for i in sortdict]))
# print sortdict
# dictiout.close()
# 
# 
# 
# #for spreadsheet
# for item in yeslist_words:
#     print item
    
later=time.time()
runtime=later-now

print 'time has passed', runtime/60


os.system('say "your program has finished"')