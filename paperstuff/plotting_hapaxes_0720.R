#plotting the hapax frequencies for ment and all words
setwd('/Users/ps22344/Desktop/rplots')

spread=read.csv('/Users/ps22344/Downloads/ota/outputfiles/hapaxes_17_25 7_20.csv', header=T);

summary(spread)
print (spread[order(spread$X), ])
#R> dd[ order(-dd[,4], dd[,1]), ]

png('hapaxes.png',  width=960, height=640, res=100)
barplot(spread[order(spread$X), ]$freqpermil, names.arg=(spread$X), main="Hapaxes per mio words, all words")
dev.off()
