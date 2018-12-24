library(ggplot2)

#histogram sales
dev.new(width=18, height=10)
p<-qplot(train$Sales,
      geom="histogram",
      binwidth = 800,  
      main = "Histogram for Sales", 
      xlab = "Sales",
      ylab = "Frequency", 
      fill=I("blue"), 
      col=I("red"),
      alpha=I(.2))

print(p)

par(ask=TRUE)

library(gridExtra)
library(ggplot2)

#plot mean of sales over the year
meanSales <- tapply(train$Sales,train$DateMonth,mean)
ggdata<-data.frame(meanSales)
p1 <- ggplot(ggdata, aes(x=as.factor(1:length(meanSales)), y=meanSales)) + geom_bar(position='dodge', stat='identity',colour="grey", fill="#009999", width=.5)+ xlab("Months") + ylab("Mean of Sales")+ ggtitle("Mean Sales across Year")+theme(plot.margin=unit(c(8,1,8,1),"cm"))

#plot mean of sales over the month
meanSales <- tapply(train$Sales,train$DateDay,mean)
ggdata<-data.frame(meanSales)
p2 <- ggplot(ggdata, aes(x=as.factor(1:length(meanSales)), y=meanSales)) + geom_bar(position='dodge', stat='identity',colour="grey", fill="#009999", width=.5)+ xlab("Day of Month") + ylab("Mean of Sales")+ ggtitle("Mean Sales across Month")+theme(plot.margin=unit(c(8,0,8,0),"cm"))

#plot mean of sales over the week
meanSales <- tapply(train$Sales,train$DayOfWeek,mean)
ggdata<-data.frame(meanSales)
p3 <- ggplot(ggdata, aes(x=as.factor(1:length(meanSales)), y=meanSales)) + geom_bar(position='dodge', stat='identity',colour="grey", fill="#009999", width=.5)+ xlab("Day of Week") + ylab("Mean of Sales")+ ggtitle("Mean Sales across Week")+theme(plot.margin=unit(c(8,1,8,1),"cm"))

#multiple plots in a single graph
library(gridExtra)
grid.arrange(p1, p2, p3, ncol=3,widths = c(2/7, 3/7, 2/7))
