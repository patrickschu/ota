##manipulating spreadsheets

import pandas as pd
import codecs
import numpy as np

inputfile='/Users/ps22344/Downloads/ota-master/alllist_0623_corrected_regex.txt'

def extractor (input_file, starttime, endtime, criterion):
	spread = pd.read_table(codecs.open(input_file, "r", "utf-8"), header=None)
	#print spread.describe()

	spread[1].astype('int')
	print "before" 
	print spread[1]
	#df[df > 0]
	#df[df['coverage'] > 50]
	# here we can add the thing from TXGDP selector
	result= spread[(spread[1] > int(starttime)) & (spread[1] < int(endtime))]
	print result.describe()
	print "after" 
	print result
	outputfile=codecs.open(inputfile+"_pandas_"+"to".join([str(i) for i in [starttime, endtime]])+".txt", "w")
	result.to_csv(outputfile, sep="\t", header=False)
	print "written to", outputfile
	

extractor(inputfile, 1599, 1700,"assi")
