
#lets investigate the pos

ment=read.csv("/Users/ps22344/Downloads/ota-master/output0703.csv", header=T);
summary(ment$wordcount);
colnames(ment);
ment$nouncount=as.numeric(ment$nouncount);
ment$wordcount=as.numeric(ment$wordcount);

#excluding poetry
ment=subset(ment, ment$genre != 'poetry');
summary(ment)

#now: noun ratio by year
nouns=aggregate(ment$nouncount, list(ment$pubdate), sum);
colnames(nouns) =c("pubdate", "nouncount");
nouns;
words=aggregate(ment$wordcount, list(ment$pubdate), sum);
colnames(words) =c("pubdate", "wordcount");
words;
merger=merge(nouns, words, by="pubdate");
merger;
merger$freq=merger[['nouncount']]/merger[['wordcount']];
merger;

setwd("Desktop/plots");
genres=levels(ment$genre);
genres=genres[-17]
print (length(genres))
count=1;
cat("mean", mean(merger$freq)*1000000)
cat("median", median(merger$freq)*1000000)
cat("sd", sd(merger$freq)*1000000)

##all in one plot
png(paste("allgenres", "nouns_ment.png"), width=960, height=640, res=100);
plot(merger$pubdate, merger$freq*1000000, ylim=c(170000,300000), ylab="Nouns per million words", xlab="Year");
print ("overall model");
modi=lm(merger$freq*1000000~merger$pubdate);
summary(modi);
abline(modi, lty=count, lwd=1.5);
legendvector=c("overall");
ltyvector=c(count);
count=count+1;
for (g in genres)
	{
	print (g);
	subset=ment[ment$genre==g,];
	print (nrow(subset));
	nouns=aggregate(subset$nouncount, list(subset$pubdate), sum)
	print ("1")
	colnames(nouns) =c("pubdate", "nouncount")
	words=aggregate(subset$wordcount, list(subset$pubdate), sum)
	print ("2")
	colnames(words) =c("pubdate", "wordcount")
	merger=merge(nouns, words, by="pubdate")
	print ("merged")
	merger
	merger$freq=(merger[['nouncount']]/merger[['wordcount']])
	print ('frequed')	
			if (nrow(subset) > 200)
	 {
		print ("range");
		print (range(merger$freq));
		print (g);
		points(merger$freq*1000000, merger$pubdate,col=count);
		lmodel=lm(merger$freq*1000000 ~ merger$pubdate);
		print (summary(lmodel));
		abline(lmodel, lty=count);
		legendvector=c(legendvector, g);
		ltyvector=c(ltyvector, count);
		count=count+1;
		print ("-------")
	}
}
legend('topright', legend=legendvector, lty=ltyvector, lwd=c(1.5,1,1,1));
dev.off()
