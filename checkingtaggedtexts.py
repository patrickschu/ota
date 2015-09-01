#this reads in the files and sees if tagging was successful
import os; import codecs; import shutil

t=os.listdir("files_tobechecked")
#read in and see which are failures
failures=[]
for item in t:
  f=codecs.open("files_tobechecked\\"+item, "r", "utf-8")
	text=f.read()
	if not text.endswith("</text>"):
	  failures.append(item)
	f.close()


#move non-failures to happy place
for item in t:
	if item not in failures:
		shutil.copy("files_tobechecked\\"+item, "files_good\\"+item)
