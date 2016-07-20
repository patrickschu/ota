#this reads authors including age

import codecs
import re


ll=[]
variables=[]

f=codecs.open("files/goodfiles_68.txt", "r", "utf-8")
for line in f:
	ll.append(line.rstrip("\n"))
f.close()

f=codecs.open("files/yeslist_regex_610.txt", "r", "utf-8")
for line in f:
	variables.append(line.rstrip("\n").split("\t"))
f.close()


for item in variables:
	print item[0]
	
for item in ll:
	try:
		#we open the corpus fils&read it
		finput=codecs.open("xmldownload_411//"+str(item)+".txt", "r", "utf-8")
		text=finput.read()
		outputfile="authors_84"
		#we get the metadata
		extractotanumber=re.compile(r'<otanumber=(.*?)>')
		extractfilenumber=re.compile(r'<no=(.*?)>')
		extracttext=re.compile(r'<text>(.*?)</text>', re.DOTALL)
		extractpubdate=re.compile(r'<pubdate=(.*?)>')
		extractgenre=re.compile(r'<genre1=(.*?)>')
		otatitleextract=re.compile(r'<otatitle=(.*?)>')
		authorextract=re.compile(r'<author=(.*?)>')
		agextract=re.compile(r'<authorage=(.*?)>')
		
		#results
		otanumber=extractotanumber.findall(text)
		filenumber=extractfilenumber.findall(text)
		pubdate=extractpubdate.findall(text)
		genre=extractgenre.findall(text)
		title=otatitleextract.findall(text)
		content=extracttext.findall(text)
		author=authorextract.findall(text)
		age=agextract.findall(text)
		#splitting here
		contentsplit=re.split(r'\W+', content[0])
		#print contentsplit[100:200]
		#print "\n\n*************\n\n"
		#setting up the output file
		output1=codecs.open(outputfile+".txt", "a", "utf-8")
		#setting up the list for the findings for each text
		results=[]
		#a list of the words well be searching for, to be used in regex
		#write the item from ll, write filenumber etc, add tab for separator
		output1.write(unicode(item)+"\t"+author[0]+"\t"+age[0]+"\n")
		output1.close()
	except IOError, err:
		print "Sorry", err
		
