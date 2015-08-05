#remember that arguments have to be strings

mentplotter=function(filename,decade) {
ment=read.csv(file.choose(), header=T)
i=c(10:length(colnames(ment)))
setwd("~/Desktop/rplots")
for (item in i) {print (colnames(ment)[item]); jpeg (paste(as.character(colnames(ment)[item]),"_",as.character(decade), "s.jpg"));  formula=tapply(ment[,item], ment$pubdate, sum)/tapply(ment$wordcount, ment$pubdate, sum); plot(formula*1000000,xaxt="n", main=colnames(ment)[item], ylab="Mean Frequency per Word"); xnames=names(formula);axis(1,at=1:length(xnames), labels=xnames); dev.off()}
}
