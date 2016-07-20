import codecs
import re


def gaddcomparer(input_file, comparison_file):
	"""
	This is used to delete entries that have been "tabbed" in previous analysis as non-relevant from the gadd list. 
	"""
	with codecs.open(input_file, "r", "utf-8") as gaddfile:
		gaddfile=gaddfile.read().split("\n")

	with codecs.open(comparison_file, "r", "utf-8") as metadatafile:
		metadatafile=metadatafile.read()
	result=[]
	
	for tuple in gaddfile:
		entry=tuple.split(",")
		#print len(entry), entry
		if entry[0].startswith("\t"):
			print "passing", entry
			pass
		else:
			entry=entry[0].strip("(u\"\'")
			if entry not in re.split("\n|\t", metadatafile):
				print "this is not in metadata", entry
			else:
				print "this is in metadata", entry
				result.append([entry, re.split("\n|\t",metadatafile)[re.split("\n|\t", metadatafile).index(entry)+1]])
		print len(result)
		outputfile=codecs.open("gadds_yeslist_withzeros_0710.txt", "w", "utf-8")
		outputfile.write("\n".join(["\t".join(r) for r in result]))
	print "written to {}".format(outputfile)

	

gaddcomparer('/Users/ps22344/Desktop/project/gadd_zerowordschecked.txt', '/Users/ps22344/Downloads/ota-master/paperstuff/alllist_0708_corrected_regex.txt')	
