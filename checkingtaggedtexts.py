#this reads in the files and sees if tagging was successful
import os; import codecs

t=os.listdir("files_tobechecked")

failures=[]
for item in t:
  f=codecs.open("files_tobechecked\\"+item, "r", "utf-8")
	text=f.read()
	if not text.endswith("</text>"):
	  failures.append(item)
	f.close()


