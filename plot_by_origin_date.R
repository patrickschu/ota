

#we have acquired intercepts and slopes, now we plot them
setwd("Desktop/rplots")


overall= c(-17800.62,10.42)
firstcentury= c( -4878.90 , 2.86 );
secondcentury= c(-11295.445279, 6.609997 );
thirdcentury= c(-3553.138 , 2.082  );

periods= list(firstcentury, secondcentury, thirdcentury);
print (firstcentury[1]);

png("allgenres_byfirstcitation.png", width=960, height=640, res=100)
plot(overall,  ylim=c(0,2500), xlim=c(1700,1800));
abline(overall[1], overall[2], lty=1);

ltyvector=c(1)
count=2

for (p in periods)
{
	cat ('intercept', p[1], 'slope', p[2],'\n');
	abline(p[1], p[2], lty=count);
	
	ltyvector=c(ltyvector, count);
	
	count=count+1;
	
}

legend('topright', legend=c("overall", "first citation 1400-1499", "first citation  1500-1599", "first citation  1600-1699"), lty=ltyvector)


dev.off()