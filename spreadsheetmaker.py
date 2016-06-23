##manipulating spreadsheets

import pandas as pd
import codecs

inputfile='/Users/ps22344/Downloads/ota-master/alllist_0623_corrected.txt'

def extractor (input_file, criterion, condition):
	spread = pd.read_table(codecs.open(input_file, "r", "utf-8"), header=None)
	#print spread.describe()

	spread[1].astype('float64')
	print spread[1].dtype
	print spread[1]
	#df[df > 0]
	#df[df['coverage'] > 50]
	# here we can add the thing from TXGDP selector
	result= spread[spread[1] < 1700]
	print result.describe()
	outputfile=codecs.open(inputfile+"_pandas_"+criterion+".txt", "w")
	result.to_csv(outputfile, sep="\t")
	

extractor(inputfile, "before1700","assi")
