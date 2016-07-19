# this plots how many words originated in a given time period
# how much fun is that?

yeslist=read.csv('/Users/ps22344/Downloads/ota-master/paperstuff/alllist_0712_corrected_regex.txt', sep="\t", header=F)
summary(yeslist)
setwd("Desktop/rplots")

names(yeslist)=c('word','birth');
head(yeslist);

summary(yeslist$birth);

##per 50 years
fifties=seq(1300,1900, by= 50);
#seq(1300, 1900, by=50)
fifties
yeslist$fifties=findInterval (yeslist$birth, fifties);
yeslist$fifties
t=data.frame(table(yeslist$fifties));
names(t)=c("int", "freq");
t
# plot(t, xaxt="n", main="Nominalization per 50 years"); 
# axis(side=1, at=c(1:9), labels=fifties);
# zeros=c(1,9);
# zero=0;
# tt=data.frame("int"=zeros, "freq"=zero);
# final=rbind(t,tt);
t$int=as.character(t$int);
##WE EXCLUDE EVERYTHING BEFORE 1250 HEERE and everything after the last date
# final=subset(t, t$int != 0 && t$int !=length(fifties));
# airquality[airquality$Month == 8 & airquality$Temp > 90, ]
final=t[t$int != 0 & t$int !=length(fifties),]
final
levels(as.factor(final$int))
length(fifties)
final=final[ order(as.numeric(final$int)), ];
final;
summary(final);
png("fifty_all.png", width=480, height=480);
nrow(final);


barplot(final$freq, ylim=c(0,300), ylab="Number of types introduced", main="First occurrence by time period, 1300-1900", names.arg=(fifties[-length(fifties)]), cex.names=0.8, las=2); 
dev.off();
length(fifties[-length(fifties)]);
length(levels(as.factor(final$int)))
#per 25 years

twens=seq(1300,1800, by= 25)
length(twens)


yeslist$twennies=findInterval (yeslist$birth, twens)

t=data.frame(table(yeslist$twennies))
names(t)=c("int", "freq")t$int=as.character(t$int)
t
# zeros=c(1,2,4,12,13,17)
# zero=0
# tt=data.frame("int"=zeros, "freq"=zero)

# final=rbind(t,tt)

summary(final)
levels(as.factor(final$int))
final=final[ order(as.numeric(final$int)), ]


twens
png("twenty-five.png", width=960, height=480)
barplot(final$freq, ylab="Number of nouns created", main="Neologisms with -ment, 1400-1800", ylim=c(0,12), names.arg=c(twens)) 

axis(side=1, at=c(1:17), labels=twens)
dev.off()
print (length(twens))



# barplot(t, type='h', lwd=15, lty=1,xaxt="n", ylab="Number of nouns created", main="Neologisms with -ment, 1400-1800", ylim=c(0,12)) 
#axis(side=1, at=c(1:17), labels=twens)


##per 10 years
decades=seq(1400,1800, by= 10)
yeslist$decade=findInterval (yeslist$birth, decades)
t=xtabs(~decade, data=yeslist)
t
plot(t, xaxt="n", main="Nominalization per 10 years")
axis(side=1, at=c(1:41), labels=decades) 

#only 1700s
sub=subset(yeslist, yeslist$birth > 1699 & yeslist$birth < 1800)
summary(sub)

t=xtabs(~decade, data=sub)
t
plot(t, xaxt="n", main="Nominalization per 10 years in 16-1700s")
axis(side=1, at=c(1:41), labels=decades) 

yeslist[yeslist$decade==21, ]

write.table(sub, "yeslist_1700s.txt", sep="\t", quote=F)








