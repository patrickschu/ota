ment=read.csv("/Users/ps22344/Downloads/ota-master/output_all.csv", sep="\t", header=T)
summary(ment)
colnames(ment)
head(ment[,45])
# # 8 to 206 are the ment words
# #item=c(10:206)
setwd("Desktop/rplots")


mentwords=aggregate(rowSums(ment[,c(8:ncol(ment))]), list(ment$pubdate), sum)
mentwords
totalwords=aggregate(ment$wordcount, list(ment$pubdate), sum)
totalwords
merger=merge(mentwords, totalwords, by="Group.1")
merger$freq=merger[,2]/merger[,3]*1000000
merger
# #plot(tapply(ment$wordcount, ment$pubdate, sum), col='red')
# #summary(ment[,8])
genres=levels(ment$genre)
cols=c(0:length(levels(ment$genre)))

cols

#individual plots, not scaled. not normalized to 1 mio
for (g in genres)
	{
	print (g);
	subset=ment[ment$genre==g,];
	print (nrow(subset));
	mentwords=tapply(rowSums(subset[,c(8:ncol(ment))]), subset$pubdate, sum);
	totalwords=tapply(subset$wordcount, subset$pubdate, sum);
	if (nrow(subset) > 99)
	{
		png(paste(g, "_1500s_ment.png"));
		plot((mentwords/totalwords)*1000000);
		dev.off();
		count=count+1
	}
}

t
#all in one plot
png(paste("allgenres", ".png"), width=960, height=640, res=100);
print ("start")
count=1;
plot(merger$Group.1, merger$freq, pch=3, ylim=c(0,3500), ylab= "Frequency per million words", xlab="Year");
lmodel=lm(merger$freq ~ merger$Group.1);
print ("overall model");
print(summary(lmodel));
print (lmodel$coef)
abline(reg=lmodel, lty=count);
legendvector=c("overall");
ltyvector=c(count);
count=count+1;
for (g in genres)
	{
	#print (g);
	subset=ment[ment$genre==g,];
	#print (nrow(subset));
	mentwords=aggregate(rowSums(subset[,c(8:ncol(ment))]), list(subset$pubdate), sum);
	totalwords=aggregate(subset$wordcount, list(subset$pubdate), sum);
	merger=merge(mentwords, totalwords, by="Group.1");
	merger$freq=(merger[,2]/merger[,3])*1000000;
		
	if (nrow(subset) > 200)
	{
		print (range(merger$freq));
		print (g);
		#points(merger$Group.1, merger$freq,pch=cols[count]);
		lmodel=lm(merger$freq ~ merger$Group.1);
		abline(a=lmodel$coefficients[1], b=lmodel$coefficients[2], lty=count);
		#legend(1700,(1600-count*100), legend=g, lty=cols[count])
		print (lmodel);
		legendvector=c(legendvector, g);
		ltyvector=c(ltyvector, count)
		count=count+1
	}
	
}
legend(1700,1000, legend=legendvector, lty=ltyvector);

dev.off();
merger;
sink("models.txt", append=T);
print ("the 1700s");
model=lm(merger$Group.1 ~ merger$freq);
summary(model);
model;
sink()
# plot(mentwords/totalwords*1000000, main="ment words in black, total in red")
# totalwords

# points(totalwords/4000, col='red')