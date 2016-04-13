# we plot types
# how much fun is that?

yeslist=read.csv("/Users/ps22344/Downloads/ota-master/yeslist_regex_610.txt", sep="\t", header=F)
summary(yeslist)


names(yeslist)=c('word','count', 'birth', 'suffix', 
'something', "something_else", "different_thing", "weird_thing")
head(yeslist)

summary(yeslist$birth)

##per 50 years
fifties=seq(1400,1800, by= 50)

yeslist$fifties=findInterval (yeslist$birth, fifties)

t=xtabs(~fifties, data=yeslist)

plot(t, xaxt="n", main="Nominalization per 50 years") 
axis(side=1, at=c(1:9), labels=fifties)


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








