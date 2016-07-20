#we get the rownumbers by year

t=by(ment, ment$pubdate, rownames)

#the sampler takes the file w/ rownumbers, picks random rows as given in the function
sampler=function(datapoints,samplenumber) {
for (item in datapoints) {
randomrows=c(randomrows,sample(item, samplenumber))
}
return (randomrows)
}

#we print out pubdates to check
for (item in x) {print (ment[item,"pubdate"])}


#we make a dataset of the only the numbers found
rand=sampler(t, 5)
tt=ment[c(rand),]
summary(tt)
