##manipulating spreadsheets

import pandas as pd
import codecs
import numpy as np

inputfile='/Users/ps22344/Downloads/ota-master/paperstuff/gadds_yeslist_withzeros_0713.txt'

def extractor (input_file, starttime, endtime, criterion):
	spread = pd.read_table(codecs.open(input_file, "r", "utf-8"), header=None)
	#print spread.describe()

	spread[1].astype('int')
	print "before" 
	print spread[1]
	#df[df > 0]
	#df[df['coverage'] > 50]
	# here we can add the thing from TXGDP selector, the operator lexicon i think i meant
	result= spread[(spread[1] > int(starttime)) & (spread[1] < int(endtime))]
	print result.describe()
	print "after" 
	print result
	outputfile=codecs.open(inputfile+"_pandas_"+"to".join([str(i) for i in [starttime, endtime]])+".txt", "w")
	#note that this outputs an index! if we read it in later, set to False
	result.to_csv(outputfile, sep="\t", header=False)
	print "written to", outputfile
	

extractor(inputfile, 0000, 1700,"assi")
