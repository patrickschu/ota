mentplotter=function(filename,decade) {
ment=read.csv(file.choose(), header=T)
ment=subset(ment, ment$pubdate > 1699 & ment$pubdate < 1801)
i=c(8:length(colnames(ment)))
setwd("G:/program files/R-Portable/files")
for (item in i) {print (colnames(ment)[item]); jpeg (paste(colnames(ment)[item],"_",decade, "s.jpg"));  formula=tapply((ment[,item]/ment$wordcount)*1000000, ment$pubdate, mean); plot(formula,xaxt="n", main=colnames(ment)[item], ylab="Mean Frequency per Mio Words"); xnames=names(formula);axis(1,at=1:length(xnames), labels=xnames); dev.off()}
}


acaplotter=function(filename,decade, genres) {
ment=read.csv(file.choose(), header=T)
ment=subset(ment, ment$pubdate > 1699 & ment$pubdate < 1801)
ment=subset(ment, ment$genre == genres)
print (summary(ment))
i=c(8:length(colnames(ment)))
setwd("G:/program files/R-Portable/files")
for (item in i) {print (colnames(ment)[item]); jpeg (paste(colnames(ment)[item],"_",genres,"_",decade, ".jpg"));  formula=tapply((ment[,item]/ment$wordcount)*1000000, ment$pubdate, mean); plot(formula,xaxt="n", main=colnames(ment)[item], ylab="Mean Frequency per Mio Words"); xnames=names(formula);axis(1,at=1:length(xnames), labels=xnames); dev.off()}
}

