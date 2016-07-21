#plotting the hapax frequencies for ment and all words
setwd('/Users/ps22344/Desktop/rplots')

#MENT WORDS

outputfile='hapaxes_25_years_ment.png'
spread=read.csv('/Users/ps22344/Downloads/ota/outputfiles/hapaxes_25yearperiods_ment_13_39_07_21.csv ', header=T);

summary(spread)
print (spread[order(spread$X), ])
#R> dd[ order(-dd[,4], dd[,1]), ]

png(outputfile,  width=960, height=640, res=100)
barplot(spread[order(spread$X), ]$freqpermil, names.arg=(spread$X), main="Hapaxes per mio words, -ment words")
dev.off()


#ALL WORDS
outputfile="hapaxes_25years_overall.png"
spread=read.csv('/Users/ps22344/Downloads/ota/outputfiles/hapaxes_25yearperiods_overall_13_50_07_21.csv', header=T);

summary(spread)
print (spread[order(spread$X), ])
#R> dd[ order(-dd[,4], dd[,1]), ]

png(outputfile,  width=960, height=640, res=100)
barplot(spread[order(spread$X), ]$freqpermil, names.arg=(spread$X), main="Hapaxes per mio words, -all words")
dev.off()


