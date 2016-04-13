ment=read.csv("/Users/ps22344/Downloads/ota-master/output0414_1700s.csv", sep="\t", header=T)
summary(ment$wordcount)
colnames(ment)
# # 8 to 206 are the ment words
# #item=c(10:206)
setwd("Desktop/plots")


mentwords=aggregate(rowSums(ment[,c(8:ncol(ment))]), list(ment$pubdate), sum)
totalwords=aggregate(ment$wordcount, list(ment$pubdate), sum)
merger=merge(mentwords, totalwords, by="Group.1")
merger$freq=merger[,2]/merger[,3]
merger
# #plot(tapply(ment$wordcount, ment$pubdate, sum), col='red')
# #summary(ment[,8])
genres=levels(ment$genre)
cols=c(0:length(levels(ment$genre)))
count=1
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

#all in one plot
png(paste("allgenres", "_1500s_ment.png"))
plot(merger$Group.1, merger$freq,  type="n", ylim=c(0,1500))

for (g in genres)
	{
	print (g);
	subset=ment[ment$genre==g,];
	print (nrow(subset));
	mentwords=aggregate(rowSums(subset[,c(8:ncol(ment))]), list(subset$pubdate), sum)
	totalwords=aggregate(subset$wordcount, list(subset$pubdate), sum)
	merger=merge(mentwords, totalwords, by="Group.1")
	merger$freq=(merger[,2]/merger[,3])*1000000
		
			if (nrow(subset) > 99)
	{
		print (range(merger$freq));
		print (g, col=cols[count])
		#points(merger$Group.1, merger$freq,col=cols[count]);
		lmodel=lm(merger$freq ~ merger$Group.1)
		abline(lmodel, col=cols[count])
		print (lmodel)
		count=count+1
	}
}
dev.off()
merger
sink("models.txt", append=T)
print ("the 1700s")
model=lm(merger$Group.1 ~ merger$freq)
summary(model)
model
sink()
# plot(mentwords/totalwords*1000000, main="ment words in black, total in red")
# totalwords

# points(totalwords/4000, col='red')