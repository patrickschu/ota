
#lets investigate the pos

ment=read.csv("/Users/ps22344/Downloads/ota-master/output0412.csv", header=T)
summary(ment$wordcount)
colnames(ment)
ment$nouncount=as.numeric(ment$nouncount)
ment$wordcount=as.numeric(ment$wordcount)


#now: noun ratio by year
nouns=aggregate(ment$nouncount, list(ment$pubdate), sum)
colnames(nouns) =c("pubdate", "nouncount")
nouns
words=aggregate(ment$wordcount, list(ment$pubdate), sum)
colnames(words) =c("pubdate", "wordcount")
words
merger=merge(nouns, words, by="pubdate")
merger
merger$freq=merger[['nouncount']]/merger[['wordcount']]

setwd("Desktop/plots")
genres=levels(ment$genre)
genres
cols=c(0:length(levels(ment$genre)))
count=1

# #all in one plot
png(paste("allgenres", "_ment.png"))
plot(merger$pubdate, merger$freq,  type="n", ylim=c(0,0.3))

for (g in genres[2:24])
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
	merger$freq=(merger[['nouncount']]/merger[['wordcount']])
	print ('frequed')	
			if (nrow(subset) > 99)
	{
		print (range(merger$freq));
		print (g, col=cols[count])
		#points(merger$Group.1, merger$freq,col=cols[count]);
		lmodel=lm(merger$freq ~ merger$pubdate)
		print (summary(lmodel))
		abline(lmodel, col=cols[count])
		count=count+1
	}
}
dev.off()

modi=lm(merger$freq~merger$pubdate)
summary(modi)



# plot(merger$pubdate, merger$freq, main="Noun ratio")
# abline (lm(merger$freq~merger$pubdate), col='red')





# # 8 to 206 are the ment words
# #item=c(10:206)
#setwd("Desktop/plots")
# mentwords=aggregate(rowSums(ment[,c(8:206)]), list(ment$pubdate), sum)
# totalwords=aggregate(ment$wordcount, list(ment$pubdate), sum)
# merger=merge(mentwords, totalwords, by="Group.1")
# merger$freq=merger[,2]/merger[,3]
# merger
# # #plot(tapply(ment$wordcount, ment$pubdate, sum), col='red')
# # #summary(ment[,8])
# genres=levels(ment$genre)
# cols=c(0:length(levels(ment$genre)))
# count=1
# cols

# #individual plots, not scaled. not normalized to 1 mio
# # for (g in genres)
	# # {
	# # print (g);
	# # subset=ment[ment$genre==g,];
	# # print (nrow(subset));
	# # mentwords=tapply(rowSums(subset[,c(8:206)]), subset$pubdate, sum);
	# # totalwords=tapply(subset$wordcount, subset$pubdate, sum);
	# # if (nrow(subset) > 99)
	# # {
		# # png(paste(g, "_ment.png"));
		# # plot(mentwords/totalwords);
		# # dev.off();
		# # count=count+1
	# # }
# # }

# #all in one plot
# png(paste("allgenres", "_ment.png"))
# plot(merger$Group.1, merger$freq,  type="n", ylim=c(0,1500))

# for (g in genres)
	# {
	# print (g);
	# subset=ment[ment$genre==g,];
	# print (nrow(subset));
	# mentwords=aggregate(rowSums(subset[,c(8:206)]), list(subset$pubdate), sum)
	# totalwords=aggregate(subset$wordcount, list(subset$pubdate), sum)
	# merger=merge(mentwords, totalwords, by="Group.1")
	# merger$freq=(merger[,2]/merger[,3])*1000000
		
			# if (nrow(subset) > 99)
	# {
		# print (range(merger$freq));
		# print (g, col=cols[count])
		# #points(merger$Group.1, merger$freq,col=cols[count]);
		# lmodel=lm(merger$freq ~ merger$Group.1)
		# abline(lmodel, col=cols[count])
		# print (lmodel)
		# count=count+1
	# }
# }
# dev.off()

# model=lm(ment$wordcount ~ ment$pubdate)
# model
# # plot(mentwords/totalwords*1000000, main="ment words in black, total in red")
# # totalwords

# # points(totalwords/4000, col='red')