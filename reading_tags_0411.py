import codecs, re, time, os, nltk, string, csv
from string import punctuation
#import unicodewriter_csv
#from unicodewriter_csv import UnicodeWriter

import csv, codecs, cStringIO

class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


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
goodfiles.remove('537')

assis=[]
dir=os.path.join("/Users","ps22344", "Downloads", "ota_0221")
#goodfiles=[i for i in os.listdir(dir) if not i.startswith(".")]
#goodfiles=['2053_tagged_13.txt']



#setting up the output file
outputname="output0412.csv"
outputfile=open(outputname, "a")
csvwriter=UnicodeWriter(outputfile, dialect='excel')

#output column names
cols=['uniq', 'filenumber', 'otanumber', 'pubdate', 'genre', 'title', 'wordcount','nouncount']



def main(filis):
	print "start"
	csvwriter.writerow(cols)
	for fili in filis:
		print fili
		inputtext=codecs.open(os.path.join(dir,fili+"_tagged.txt"), "r", "utf-8").read()
		text=adtextextractor(inputtext, fili)
		#this is a standin for word count; maybe re-consider??
		taggedtext=postagextractor(text, fili)
		wordcount=unicode(len(taggedtext))
		print "\n----\nwordcount", wordcount
		tags_to_count=["u'NNP'", "u'NNPS'", "u'NN'", "u'NNS'"]
		#stolen from here http://stackoverflow.com/questions/11740814/is-there-a-way-to-use-two-if-conditions-in-list-comprehensions-in-python
		counted_tags=[i for i in taggedtext if any(x in i for x in tags_to_count)]
		nouncount=unicode(len(counted_tags))
		print "nouncount", nouncount
		#ll=[i for i in taggedtext if "u'NNP'" in i in tags_to_count]
		#we get the metadata
		otanumber=tagextractor(inputtext, "otanumber", fili )
		filenumber=tagextractor(inputtext, "no", fili )
		pubdate=tagextractor(inputtext, "pubdate", fili )
		genre=tagextractor(inputtext, "genre1", fili )
		title=tagextractor(inputtext, "otatitle", fili)
		#a list of the words well be searching for, to be used in regex
		#write the item from ll, write filenumber etc, add tab for separator
		outputlist=[unicode(fili), filenumber, otanumber, pubdate, genre, title, wordcount, nouncount]
		csvwriter.writerow(outputlist)
	print "finish"
		
main(goodfiles)
		# print "text is {} items long".format(len(t))
# 	for number in range(10):
# 		print number
# 		tt=[i for i in t if len(i) == number]
# 		print "For {}, there are {} instances".format(number, len(tt))
	
	