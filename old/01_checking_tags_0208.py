#this reads in the files and sees if tagging was successful
import os; import codecs; import shutil

print "start"

t=[i for i in os.listdir("/Users/ps22344/Downloads/ota_0208") if not i.startswith(".")]
#read in and see which are failures
#were readin in files to see if all accurately tagged
print "files", len(t)
failures=[]
for item in t:
	filename=os.path.join("/Users/ps22344/Downloads/ota_0208", item)
	#filename="Users/ps22344/Downloads/ota_0208/"+item
	f=codecs.open(filename, "r", "utf-8")
	text=f.read()
	if not text.endswith("</text>"):
		print item
		failures.append(item)
		t=raw_input(" Do it ")
	f.close()

print len(failures)

# #move non-failures to happy place
# for item in t:
# 	if item not in failures:
# 		shutil.copy("files_tobechecked\\"+item, "files_good\\"+item)
# 
# 
# #compare original to tagged 
# #fili comes from goodfiles
# for item in fili:
# 	try:
# 		f=open("tagged_92//"+item+"_tagged.txt", "r")
# 		f.close()
# 	except:
# 		print item
		
		
print "end"
