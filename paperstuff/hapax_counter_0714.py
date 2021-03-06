# -*- coding: utf-8 -*-

##TESTING###

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


##VARIABLES
now=time.time()
otadir=os.path.split(os.getcwd())[0]
header="\n\n-------\n"
#these are words to iterate over
yeslist=[]
yesdict={}
f=codecs.open("/Users/ps22344/Downloads/ota/paperstuff/datafiles/alllist_0712_corrected_regex.txt_pandas_0to1700.txt", "r", "utf-8")
for line in f:
	yeslist.append(line.rstrip("\n").split("\t"))
f.close()
yeslist_words=[re.compile("^"+i[1]+"$") for i in yeslist]
print '# of words in yeslist: ', len(yeslist_words)
#spreadsheet of files, note that we only use this to find relevant files
inputi=pandas.read_csv('/Users/ps22344/Downloads/ota/paperstuff/datafiles/output_alllist_0713', sep="\t")


##TOOLS
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
	#it would be nice if input was just the file name and we add ending according to format
	#right now, we do ".txt.json"
	print "Starting the dictionarywriter, sorting is", sort_dict
	sorteddict=sorted(dictionary.items(), key=lambda x: x[1], reverse=True)
	with codecs.open(os.path.join(otadir, "outputfiles", file_name), "w", "utf-8") as outputi:
		outputi.write("\n".join([":".join([i[0],unicode(i[1])]) for i in sorteddict]))
	with codecs.open(os.path.join(otadir,"outputfiles", file_name+".json"), "w", "utf-8") as jsonoutputi:
		json.dump(dictionary, jsonoutputi, ensure_ascii=False)
	print "Written to",  os.path.join(otadir,"outputfiles", file_name)
	
	
def spreadmerger(spreadsheet_1, spreadsheet_2, filename=False):
	spreadsheet1=pandas.read_csv(spreadsheet_1, encoding="utf-8")
	spreadsheet2=pandas.read_csv(spreadsheet_2, encoding="utf-8")
	outputspread=pandas.concat([spreadsheet1,spreadsheet2], axis=1)
	print os.path.split(spreadsheet_1)
	outputspread.to_csv(os.path.join(otadir, "outputfiles", os.path.split(spreadsheet_1)[1]+os.path.split(spreadsheet_2)[1]+"_merged.csv"), encoding="utf-8")
	return outputspread

spreadmerger('/Users/ps22344/Downloads/ota/outputfiles/hapaxes_25yearperiods_overall_13_50_07_21.csv', '/Users/ps22344/Downloads/ota/outputfiles/hapaxes_25yearperiods_ment_13_39_07_21.csv' )


	
##MAIN HAPAX_COUNTER
def main(inputspread, start_time, end_time, interval, write_files=False):
	"""
	Creates periods between start_time and end_time as determined by interval. 
	For each, relevant texts are extracted and words are counted. 
	In the end, full dictionaries, hapax dictionaries, and ment-dictionaries are output as txt file and json.
	They are created for each time period and the entire dataset ("overall"). 
	"""
	overalldicti=defaultdict(dict)
	overalldicti_ment=defaultdict(dict)
	spreadsheet=pandas.DataFrame()
	for item in range(start_time, end_time, interval):
		print header, item, header
		subsetspread= periodfinder(inputspread, item, interval) 
		perioddicti= defaultdict(list)
		#iterating over all the files contained in the extracted spreadsheet
		for fileno in [f for f in subsetspread['filenumber']]:
			#read file
			with codecs.open(os.path.join('/Users/ps22344/Downloads/ota_0621', unicode(fileno)+".txt"), "r", "utf-8") as inputfili:
				inputtext=inputfili.read()
			content=adtextextractor(inputtext,item)
			#print "original", content[:20000]
			content=re.sub(u"(—|-)", " ", content)
			#print header, header, "new", content[:20000]
			contentsplit=nltk.tokenize.word_tokenize(content, language='english')
			text= [i.lower() for i in contentsplit if not re.match(r"\d+", i)]
			text= [re.sub(r"('s|s|s's|ed)\b", "", i) for i in text if i not in string.punctuation]
			text= [re.sub(r"(\.+|'+|,+|\*+)", "", i, re.UNICODE) for i in text]
			for word in text:
				perioddicti[word].append(word)
		print header, "Number of words in perioddicti is", len(perioddicti)
		"""
		we need three dicts:
		--for the present period--
		the perioddicti contains lists per wordcounts for this period
		the perioddicti_nos contains counts per word for this period, based on perioddicti
		the perioddicti_ment contains overall wordcounts for all mentwords, based on the perioddicti_nos
		the perioddicti_hapax contains all hapaxes for this period, based on perioddicti_nos
		--overall--
		the overalldicti  contains counts for each word per period, format: {word:{year1:X, year2:x ...}, word2:{}}
		the overalldicti_ment containts count for each mentword per period, format cf above
		the overalldicti_hapax (created later) contains all the hapaxes total, based on overalldicti
		overalldicti_hapax_ment (created later) contains all the hapaxes in -ment total, based on overalldicti_hapax
		"""
		perioddicti_nos={k:len(v) for k,v in perioddicti.items()}
		perioddicti_hapax= {k:v for k,v in perioddicti_nos.items() if v == 1}
		perioddicti_ment= {k:v for k,v in perioddicti_nos.items() if any (re.match(regex,k) for regex in yeslist_words)}
		
		
		for entry in perioddicti:
			overalldicti[entry][item]=perioddicti_nos[entry]
		for entry in perioddicti_ment:
			overalldicti_ment[entry][item]=perioddicti_ment[entry]
		
		if write_files:
			print "Write to file"
			dictwriter(unicode(item)+"to"+unicode(item+interval-1)+"_hapaxdict.txt", perioddicti_hapax)
			dictwriter(unicode(item)+"to"+unicode(item+interval-1)+"_dict.txt", perioddicti_nos)
			dictwriter(unicode(item)+"to"+unicode(item+interval-1)+"_mentdict.txt", perioddicti_ment)
	
	print "Making hapaxdicti"	
	overalldicti_hapax={k:v for k,v in overalldicti.items() if sum(v.values()) == 1}
	overalldicti_hapax_ment={k:v for k,v in overalldicti_hapax.items() if any (re.match(regex,k) for regex in yeslist_words)}
	print "Overall hapax has {} entries".format(len(overalldicti_hapax))
	if write_files:	
		print "Write to file"
		dictwriter(unicode(start_time)+"to"+unicode(end_time)+"int"+unicode(interval)+"_overall_hapaxdict.txt", overalldicti_hapax)
		dictwriter(unicode(start_time)+"to"+unicode(end_time)+"int"+unicode(interval)+"overall_dict.txt", overalldicti)
		dictwriter(unicode(start_time)+"to"+unicode(end_time)+"int"+unicode(interval)+"overall_mentdict.txt", overalldicti_ment)
		dictwriter(unicode(start_time)+"to"+unicode(end_time)+"int"+unicode(interval)+"overall_hapax_mentdict.txt", overalldicti_hapax_ment)

	
##HAPAX_STATS MAKER	
def hapax_stats(output_file, hapax_file, allwords_file, write_file=False):
	"""
	The hapax_stats creates a spreadsheet calculating ratios hapax to total words. 
	hapax_file is a dictionary of hapaxes per year, allwords_file is a dictionary of total words per year. 
	Input needs to be a JSON file, formatted: {entry: {year1:count, year2:count, ...}, entry2:{}}.
	"""
	otadir=os.path.split(os.getcwd())[0]
	hapax_periods=defaultdict(list)
	allwords_periods=defaultdict(list)
	with open(hapax_file) as inputfile:
		hapaxes=json.load(inputfile, encoding='utf-8')
	with open(allwords_file) as inputfile:
		allwords=json.load(inputfile, encoding='utf-8')
	#this is set comprehension, cf here: http://stackoverflow.com/questions/30331907/list-comprehension-check-if-item-is-unique
	periods={v.keys()[0] for k,v in allwords.items()}
	#building dictionaries
	for p in periods:
		for entry in hapaxes:
			hapax_periods[p]=hapax_periods[p]+[v for k,v in hapaxes[entry].items() if k==p ]
	hapax_periods={k:sum(v) for k,v in hapax_periods.items()}
	hapax_periods[u'overall']=sum(hapax_periods.values())
	print header, "The Hapax dictionary\n", hapax_periods
	for p in periods:
		for entry in allwords:
			allwords_periods[p]=allwords_periods[p]+[v for k,v in allwords[entry].items() if k==p ]
	allwords_periods={k:sum(v) for k,v in allwords_periods.items()}
	allwords_periods[u'overall']=sum(allwords_periods.values())
	print header, "The overall dictionary\n", allwords_periods

	hapaxspread=pandas.DataFrame.from_dict(hapax_periods, orient='index')
	hapaxspread.columns=['hapaxes']
	print hapaxspread
	
	
	allwordsspread=pandas.DataFrame.from_dict(allwords_periods, orient='index')
	allwordsspread.columns=['wordcount']
	print allwordsspread
	
	fullspread = pandas.concat([hapaxspread,allwordsspread], axis=1)
	print fullspread
	fullspread['freqpermil']=fullspread['hapaxes']/fullspread['wordcount']*1000000
	fullspread=fullspread.sort_index()
	print header, fullspread
	if write_file:
		fullspread.to_csv(os.path.join(otadir, "outputfiles", output_file+"_"+time.strftime("%H_%M_%m_%d")+".csv"), encoding="utf-8")
		print "Written", os.path.join(otadir, "outputfiles", output_file+"_"+time.strftime("%H_%M_%m_%d")+".csv")
		
		
#hapax_stats('hapaxes_25yearperiods_overall', '/Users/ps22344/Downloads/ota/outputfiles/1700to1800int25_overall_hapaxdict.txt.json', '/Users/ps22344/Downloads/ota/outputfiles/1700to1800int25overall_dict.txt.json', write_file=True)

#main(inputi, 1700, 1800, 25, True)




    
later=time.time()
runtime=later-now

print 'time has passed', runtime/60


#os.system('say "your program has finished"')