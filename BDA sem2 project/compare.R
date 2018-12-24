#Compare both models for particular store
compareModels <- function(StoreID){
	
	storedata <- train.list[[StoreID]]
	indexes <- sample(1:nrow(storedata),size=0.2*nrow(storedata))

	#call both ARIMA and neural network models for the store
	errA <- storeArima(StoreID,indexes=indexes,plots=FALSE)
	errN <- storeNN(StoreID,indexes=indexes,plots=FALSE)

	cat("\n-----------------------------\n")
	cat("Arima RMSE:",round(errA,5),"\n")
	cat("Neural Network RMSE:",round(errN,5))
	cat("\n-----------------------------\n")

	data1 <- read.csv("./Rossmann Data/Arimapredictedsales.csv")
	data2 <- read.csv("./Rossmann Data/NNpredictedsales.csv")

    Date <- storedata[indexes,"Date"]

	#plot observed and predicted sales of test data	
	dev.new(width=18, height=10)
    plot(Date,data1$Sales,type="h",xlab="Date",ylab="Sales",col='red',main=paste("Sales of store ",StoreID),xaxp=c(min(Date),max(Date),5))
    lines(Date,data1$PredictedSales,type="p",col='green',lwd=2)
    lines(Date,data2$PredictedSales,type="p",col='blue',lwd=2)
    legend('topleft',legend=c("Observed","Predicted (Arima)","Predicted (Neural Network)"),col=c('red','green','blue'),cex=0.8,pch=c(20,21,21),lwd=2) 
    
}
