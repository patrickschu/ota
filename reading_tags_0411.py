import codecs, re, time, os, nltk, string
from string import punctuation



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
    
def postagextractor(text, fili):
	cleantext=re.sub("\)\(", ") (", text)
	print "text is {} words long".format(len(text.split(" ")))
	result=[tuple(i.split(", ")) for i in cleantext.split(") (")]
	test= [i for i in result if len(i) != 2]
	if len(test) > 0:
		print "alarm postagextractor, tags longer than 2 items discovered"
		print test
		assis.append(fili)
	return result
	

#reading in the yestlist, nolist or whatever. these are the words to iterate over/search for
yeslist=[]
f=open("yeslist_regex_610.txt", "r")

for line in f:
	yeslist.append(line.rstrip("\n").split("\t"))
	
f.close()

print "{} words in yeslist".format(len(yeslist))

#this is the list with the files/books we're using
goodfiles=[]
f=open("goodfiles_68.txt", "r")

for line in f:
	goodfiles.append(line.rstrip("\n"))

f.close()
print "{} files in goodfiles".format(len(goodfiles))

print os.getcwd()
assis=[]
dir=os.path.join("/Users","ps22344", "Downloads", "ota_0221")
goodfiles=[i for i in os.listdir(dir) if not i.startswith(".")]
#goodfiles=['2053_tagged_13.txt']



#setting up the output file
outputfile="output0411.csv"
output0=codecs.open(outputfile, "a", "utf-8")
#output column names
cols=['uniq', 'filenumber', 'otanumber', 'pubdate', 'genre', 'title', 'wordcount','nouncount\n']
output0.write("\t".join(cols)+"\t")
output0.close()

def main(filis):
	for fili in filis:
		print fili
		inputtext=codecs.open(os.path.join(dir,fili), "r", "utf-8").read()
		text=adtextextractor(inputtext, fili)
		#this is a standin for word count; maybe re-consider??
		taggedtext=postagextractor(text, fili)
		wordcount=str(len(taggedtext))
		tags_to_count=["u'NNP'", "u'NNPS'", "u'NN'", "u'NNS'"]
		#stolen from here http://stackoverflow.com/questions/11740814/is-there-a-way-to-use-two-if-conditions-in-list-comprehensions-in-python
		counted_tags=[i for i in taggedtext if any(x in i for x in tags_to_count)]
		result=str(len(counted_tags))
		#ll=[i for i in taggedtext if "u'NNP'" in i in tags_to_count]
		#we get the metadata
		otanumber=tagextractor(inputtext, "otanumber", fili )
		filenumber=tagextractor(inputtext, "no", fili )
		pubdate=tagextractor(inputtext, "pubdate", fili )
		genre=tagextractor(inputtext, "genre1", fili )
		title=tagextractor(inputtext, "otatitle", fili)
		
		#a list of the words well be searching for, to be used in regex
		#write the item from ll, write filenumber etc, add tab for separator
		outputlist=[unicode(fili), filenumber, otanumber, pubdate, genre, title, wordcount, result]
		output1=codecs.open(outputfile, "a", "utf-8")
		output1.write("\t".join(outputlist)+"\n")
		output1.close()
		
main(goodfiles)
		# print "text is {} items long".format(len(t))
# 	for number in range(10):
# 		print number
# 		tt=[i for i in t if len(i) == number]
# 		print "For {}, there are {} instances".format(number, len(tt))
	
	