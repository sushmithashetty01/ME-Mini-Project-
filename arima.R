library(SimDesign)
library(forecast)

#Implement ARIMA model for the required store
storeArima <- function(StoreID,indexes=NULL,plots=TRUE){
    
    storedata <- train.list[[StoreID]]
 
    #split the given data into training and testing sets of 80:20 ratio
    if(is.null(indexes)){
        indexes <- sample(1:nrow(storedata),size=0.2*nrow(storedata))
    }
    traindata <- storedata[-indexes,]
    testdata <- storedata[indexes,]
  
    #create time series data based on sales
    train_sales <- ts(traindata$Sales,frequency=7) #data is observed daily
    test_sales <- ts(testdata$Sales,frequency=7)
   
    #set the training regressors
    z <- fourier(ts(log(traindata$Sales), frequency = 365.25),K=5)
    train_regressors <- cbind(z,traindata$Customers,traindata$Promo,traindata$SchoolHoliday) 

    #set the testing regressors
    zf <- fourier(ts(log(testdata$Sales), frequency = 365.25),K=5)
    test_regressors <- cbind(zf,testdata$Customers,testdata$Promo,testdata$SchoolHoliday)
    
    test_period <- max(testdata$Date) - min(testdata$Date) + 1
    
    #fit arima model with training data
    model <- auto.arima(train_sales,xreg=train_regressors)

    #forecast the sales using the fitted model with testing data over the test period
    forecast_test <- forecast(model,xreg=test_regressors,h=test_period)
    
    #save the predicted sales
    testdata$PredictedSales <- as.numeric(forecast_test$mean)

    if(plots){
        dev.new(width=18, height=10)
        testdata <- testdata[order(testdata$Date), ]
        #plot observed and predicted sales of test data
        plot(testdata$Date,testdata$Sales,type="h",xlab="Date",ylab="Sales",col='red',main=paste("Sales of store ",StoreID),xaxp=c(min(testdata$Date),max(testdata$Date),5))
        lines(testdata$Date,testdata$PredictedSales,type="p",col='green',lwd=1.5)
        legend('topleft',legend=c("Observed","Predicted (Arima)"),col=c('red','green'),cex=0.8,pch=c(20,21),lwd=1.5) 
    }
    # Store results in csv files
    Sales <- numeric(0)
    PredictedSales <- numeric(0)
    submission <- data.frame(Sales, PredictedSales)
    submission.tmp <- testdata[, c("Sales","PredictedSales")]
    submission <- rbind(submission, submission.tmp)
    write.table(submission, "./Rossmann Data/Arimapredictedsales.csv", sep = ",", row.names = FALSE)

    #calculate the root mean square error value to check the accuracy of the model
    err <- RMSE(testdata$Sales,testdata$PredictedSales,type='NRMSE_SD')
    err
  
}

#Function to calculate RMSE for all stores and compute average RMSE for the model 
totalRMSEA <- function(){
    num <- length(train.list)
    total <- 0

    # Set a null data frame to store results
    Id <- integer(0)
    RMSE <- numeric(0)
    submission <- data.frame(Id=Id, NRMSE=RMSE)

    for(i in 1:num){
        err <- storeArima(i,plots=FALSE)
        print(c(i,err))
        submission <- rbind(submission, data.frame(Id=i,NRMSE=err))
        total <- total+err
    }
    #save NRMSE for each store in csv file
    write.table(submission, "./Rossmann Data/Arimanrmse.csv", sep = ",", row.names = FALSE)
    print(total/num)
}
