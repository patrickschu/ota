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
yesdict={}
f=codecs.open("/Users/ps22344/Downloads/ota-master/paperstuff/alllist_0712_corrected_regex.txt_pandas_0to1700.txt", "r", "utf-8")
for line in f:
	yeslist.append(line.rstrip("\n").split("\t"))
	
f.close()

#WATCH THIS SETTING
yeslist_words=[i[1] for i in yeslist]
yeslist_words=[re.compile("^"+i[1]+"$") for i in yeslist]
print len(yeslist_words)
yesdict={i[1]:0 for i in yeslist}





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
    regex=re.compile("<text>(.*?)</text>", re.DOTALL)
    result=re.findall(regex, text)
    if len(result) != 1:
        print "alarm in adtextextractor", fili, result
    return unicode(result[0])

def dictwriter(file_name, dictionary, sort_dict=True):
	"""
	writes out a dictionary to a text file after sorting it
	"""
	print "Starting the dictionarywriter, sorting is", sort_dict
	sorteddict=sorted(dictionary.items(), key=lambda x: x[1], reverse=True)
	with codecs.open(file_name, "w", "utf-8") as outputi:
		outputi.write("\n".join([":".join([i[0],unicode(i[1])]) for i in sorteddict]))
	with codecs.open(file_name+".json", "w", "utf-8") as jsonoutputi:
		json.dump(dictionary, jsonoutputi, ensure_ascii=False)
	
header="\n\n-------\n"
	

def main(inputspread, start_time, end_time, interval, output_files=False):
	"""
	Creates periods between start_time and end_time as determined by interval. 
	For each, relevant texts are extracted and words are counted. 
	In the end, full dictionary and hapax dictionary are output as txt file and json.
	"""
	overalldicti=defaultdict(dict)
	overalldicti_ment=defaultdict(dict)
	spreadsheet=pandas.DataFrame()
	#ah this loop is too long
	for item in range(start_time, end_time, interval):
		periodnow=time.time()
		print header, item, header
		subsetspread= periodfinder(inputspread, item, interval) 
		perioddicti= defaultdict(list)
		perioddicti_ment=defaultdict()
		#iterating over all the files contained in the extracted spreadsheet
		for fileno in [f for f in subsetspread['filenumber']]:
			#read file
			with codecs.open(os.path.join('/Users/ps22344/Downloads/ota_0621', unicode(fileno)+".txt"), "r", "utf-8") as inputfili:
				inputtext=inputfili.read()
			content=adtextextractor(inputtext,item)
			content=re.sub(u"(—|-)", " ", content)
			contentsplit=nltk.tokenize.word_tokenize(content, language='english')
			text= [i.lower() for i in contentsplit if not re.match(r"\d+", i)]
			text= [re.sub(r"('s|s|s's|ed)\b", "", i) for i in text if i not in string.punctuation]
			text= [re.sub(r"(\.+|'+|,+|\*+)", "", i, re.UNICODE) for i in text]
			for word in text:
				perioddicti[word].append(word)
		print header, "Number of words in perioddicti is", len(perioddicti)
		perioddicti_nos={k:len(v) for k,v in perioddicti.items()}
		#perioddicti_ment= {k:v for k,v in perioddicti_nos.items() if any (re.match("^"+regex+"$",k) for regex in yeslist_words)}
		perioddicti_ment= {k:v for k,v in perioddicti_nos.items() if any (re.match(regex,k) for regex in yeslist_words)}
		print perioddicti_ment
		hapaxdicti= {k:v for k,v in perioddicti_nos.items() if v == 1}
		if output_files:
			dictwriter(unicode(item)+"to"+unicode(item+interval-1)+"_hapaxdict.txt", hapaxdicti)
			dictwriter(unicode(item)+"to"+unicode(item+interval-1)+"_dict.txt", perioddicti_nos)
			dictwriter(unicode(item)+"to"+unicode(item+interval-1)+"_mentdict.txt", perioddicti_ment)
		for entry in perioddicti:
			overalldicti[entry][item]=perioddicti_nos[entry]
		for entry in perioddicti_ment:
			overalldicti_ment[entry][item]=perioddicti_ment[entry]
			hapaxspread=pandas.DataFrame()
			#timing
		periodlater=time.time()
		periodruntime=periodlater-periodnow
		print "time has passed for this period", periodruntime/60
	#this is the overall dictionary and output
	print "Making hapaxdictis"	
	overallhapax={k:v for k,v in overalldicti.items() if sum(v.values()) == 1}
	menthapax={k:v for k,v in overalldicti_ment.items() if sum(v.values()) == 1}
	print "Overall hapax has {} entries".format(len(overallhapax))
	
	if output_files:
		print "Write to file"
		dictwriter(unicode(start_time)+"to"+unicode(end_time)+"overall_hapaxdict.txt", overallhapax)
		print "Writing the overalldicti to file"
		dictwriter(unicode(start_time)+"to"+unicode(end_time)+"overall_dict.txt", overalldicti)
		dictwriter(unicode(start_time)+"to"+unicode(end_time)+"ment_hapaxdict.txt", menthapax)
		dictwriter(unicode(start_time)+"to"+unicode(end_time)+"overall_mentdict.txt", overalldicti_ment)

	
def hapax_stats(hapax_file, allwords_file):
	hapax_periods=defaultdict()
	allwords_periods=defaultdict()
	with open(hapax_file) as inputfile:
		hapaxes=json.load(inputfile, encoding='utf-8')
	with open(allwords_file) as inputfile:
		allwords=json.load(inputfile, encoding='utf-8')
	
	#this is set comprehension, cf here: http://stackoverflow.com/questions/30331907/list-comprehension-check-if-item-is-unique
	periods={v.keys()[0] for k,v in allwords.items()}
	print periods
	for p in periods:
		hapax_periods[p]=len([e for e in hapaxes.values() if e.get(p, None)])
	hapax_periods[u'overall']=sum(hapax_periods.values())
	print hapax_periods
	for p in periods:
		allwords_periods[p]=[e.values()[0] for e in allwords.values() if e.get(p, None)]
		allwords_periods[p]=sum(allwords_periods[p])
	allwords_periods[u'overall']=sum(allwords_periods.values())
	print allwords_periods
	for item in hapax_periods:
		print type(item)
	hapaxspread=pandas.DataFrame(hapax_periods, index=["hapaxes"])

	allwordspread=pandas.DataFrame(allwords_periods, index=["allwords"])
	print hapaxspread, header
	print allwordspread, header
	
	# fullspread=pandas.concat([hapaxspread, allwordspread])
# 	fullspread['freqpermil']=fullspread['hapaxes']/fullspread['allwords']
# 	print header, fullspread
	
	
	fullspread=pandas.DataFrame(index=hapax_periods.keys())
	fullspread['hapaxes']=hapax_periods.values()
	fullspread['allwords']=allwords_periods.values()
	print header, fullspread
	fullspread['freqpermil']=fullspread['hapaxes']/fullspread['allwords']*1000000
	print header, fullspread
		
		
#hapax_stats('/Users/ps22344/Downloads/ota-master/1700to1800overall_hapaxdict.txt.json', '/Users/ps22344/Downloads/ota-master/1700to1800overall_dict.txt.json')
		
	
		
	#iterate over periods to 
	# get total number of words
	# number of hapaxes
	#then totaltotal number of hapaxes, totaltotal number of words



main(inputi, 1700, 1800, 10, output_files=True)

    
later=time.time()
runtime=later-now

print 'time has passed', runtime/60


os.system('say "your program has finished"')