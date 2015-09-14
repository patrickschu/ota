#reading in the yestlist, nolist or whatever. these are the words to iterate over/search for
yeslist=[]
f=open("H:\\ota\\files\\yeslist_regex_610.txt", "r")

for line in f:
	yeslist.append(line.rstrip("\n").split("\t"))
	
f.close()

#this is the list with the files/books we're using
goodfiles=[]
f=open("H:\\ota\\files\\goodfiles_68.txt", "r")

for line in f:
	goodfiles.append(line.rstrip("\n"))

f.close()


#the actual reader
for item in goodfiles:
	try:
		#we open the corpus fils&read it
		finput=codecs.open("H://ota//xmldownload_411//"+str(item)+".txt", "r", "utf-8")
		text=finput.read()
		outputfile="output914.txt"
		#we get the metadata
		extractotanumber=re.compile(r'<otanumber=(.*?)>')
		extractfilenumber=re.compile(r'<no=(.*?)>')
		extracttext=re.compile(r'<text>(.*?)</text>', re.DOTALL)
		extractpubdate=re.compile(r'<pubdate=(.*?)>')
		extractgenre=re.compile(r'<genre1=(.*?)>')
		otatitleextract=re.compile(r'<otatitle=(.*?)>')
		#results
		otanumber=extractotanumber.findall(text)
		filenumber=extractfilenumber.findall(text)
		pubdate=extractpubdate.findall(text)
		genre=extractgenre.findall(text)
		title=otatitleextract.findall(text)
		content=extracttext.findall(text)
		contentsplit=re.split(r'\W+', content[0])
		#print len(contentsplit)
		#setting up the output file
		output1=codecs.open(outputfile, "a", "utf-8")
		#setting up the list for the findings for each text
		results=[]
		#a list of the words well be searching for, to be used in regex
		#write the item from ll, write filenumber etc, add tab for separator
		output1.write(unicode(item)+"\t"+filenumber[0]+"\t"+otanumber[0]+"\t"+pubdate[0]+"\t"+genre[0]+"\t"+title[0]+"\t"+unicode(len(contentsplit))+"\t")
		output1.close()
		#print "output1 closed"
		#iterate over all metadata
		for thing in yeslist:
			#print thing[0]
			words=re.findall(r"\b("+thing[0]+"\'?)",content[0])
			results.append(words)
			#print results
			#we join the list to make it a string, add a tab as separator
			#output2.write((",").join(words)+"\t")
			#log file writing
		print "reading", item, filenumber
		#print/write results
		output3=codecs.open(outputfile, "a", "utf-8")
		#all this does is write all lengths into one list instead of listing each of 		#them. they need to be in str() for join to work for whatever reason
		output3.write("\t".join([str(len(i)) for i in results])+"\n")
		output3.close()
		logout=codecs.open(outputfile+"_log.txt", "a", "utf-8")
		logout.write(str(results)+"\n")
		logout.close()
		#print "output3 closed"
		#write a new line for each inputfile
		#output4=codecs.open(outputfile, "a", "utf-8")
		#output4.write(' \n')
		#output4.close()
		#print "output 4 closed"
		#finput.close()
	except IOError, err:
		print "Fuck you", err
