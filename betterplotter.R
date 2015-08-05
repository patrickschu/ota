#remember that arguments have to be strings

mentplotter=function(filename,decade) {
ment=read.csv(file.choose(), header=T)
i=c(8:length(colnames(ment)))
setwd("~/Desktop")
for (item in i) {print (colnames(ment)[item]); jpeg (paste(colnames(ment)[item],"_",decade, "s.jpg"));  formula=tapply(ment$menttotal, ment$pubdate, sum)/tapply(ment$wordcount, ment$pubdate, sum); plot(formula,xaxt="n", main=colnames(ment)[item], ylab="Mean Frequency per Word"); xnames=names(formula);axis(1,at=1:length(xnames), labels=xnames); dev.off()}
}
