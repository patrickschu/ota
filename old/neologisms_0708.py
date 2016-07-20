import codecs
import re

def comparer(file_1, file_2):
	"""
	The comparer takes a global file and a partially overlapping file,
	e.g. Gadd's list of neologisms and outputs the overlap.
	"""
	outputfile="yeslist_overlap_gadd_and_oed1800s_0713.txt"
	overlap=[]
	with codecs.open(file_1, "r", "utf-8") as inputfile:
		file_1=inputfile.read()
	with codecs.open(file_2, "r", "utf-8") as inputfile:
		file_2=inputfile.read()
	for item in re.split("\n|\t", file_1):
		if item in re.split("\n|\t", file_2):
			overlap.append(item)
	with codecs.open(outputfile, "w", "utf-8") as outputfile:
		outputfile.write("\n".join(overlap))
	print "donedonedone, written to", outputfile
		
		
#comparer('/Users/ps22344/Downloads/ota-master/alllist_1800s_regex.txt', '/Users/ps22344/Downloads/ota-master/outputfiles/gadds_yeslist_0707.txt')
		
def metadataadder(input_file, metadata_file):
	outputfile="yeslist_overlap_gadd_and_oed1800_metadata_added_0713.txt"
	result=[]
	with codecs.open(input_file, "r", "utf-8") as inputfile:
		input_file=inputfile.read()
	with codecs.open(metadata_file, "r", "utf-8") as inputfile:
		metadata_file=inputfile.read()
	for line in input_file.split("\n"):
		if line in re.split("\n|\t", metadata_file):
			result.append([line, re.split("\n|\t", metadata_file)[re.split("\n|\t", metadata_file).index(line)+1]])
	with codecs.open(outputfile, "w", "utf-8") as outputfile:
		outputfile.write("\n".join(["\t".join(r) for r in result]))
	print "donedonedone, written to", outputfile
		
			
		
		
metadataadder('/Users/ps22344/Downloads/ota-master/yeslist_overlap_gadd_and_oed1800s_0713.txt', '/Users/ps22344/Downloads/ota-master/paperstuff/alllist_0712_corrected_regex.txt')