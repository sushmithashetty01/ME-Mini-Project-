library(neuralnet)
library(SimDesign)

#Implement ARIMA model for the required store
storeNN <- function(StoreID,hid=4,tres=0.03,indexes=NULL,plots=TRUE) {
    storedata <- train.list[[StoreID]]

    storedata <- storedata[c('Date','Sales','Customers','Promo','SchoolHoliday')]
    storedata['SchoolHoliday'] <- storedata$SchoolHoliday==1
    storedata['Promo'] <- storedata$Promo==1

    #tranform the values by scaling them between -1 and 1
    sm1 <- mean(storedata$Sales)
    storedata$Sales <- storedata$Sales - sm1
    sm2 <- max(abs(storedata$Sales))
    storedata$Sales <- storedata$Sales / sm2

    cm1 <- mean(storedata$Customers)
    storedata$Customers <- storedata$Customers - cm1
    cm2 <- max(abs(storedata$Customers))
    storedata$Customers <- storedata$Customers / cm2

    storedata$PredictedSales <- 0

    #split the given data into training and testing sets of 80:20 ratio
    if(is.null(indexes)){
        indexes <- sample(1:nrow(storedata),size=0.2*nrow(storedata))
    }
    traindata <- storedata[-indexes,2:(ncol(storedata)-1)]
    testdata <- storedata[indexes,1:(ncol(storedata)-1)]

    #generate formula Sales ~ Customers + Promo + SchoolHoliday
    n <- names(traindata)
    f <- as.formula(paste("Sales ~", paste(n[n != "Sales"], collapse = " + ")))

    #train neural network model with one hidden layer using the training data
    model <- neuralnet(f, traindata, hidden=hid,threshold=tres,learningrate=0.01)
    if(plots){
        plot(model)
        readline()
    }

    #computer value for test data
    c <- compute(model,testdata[,3:(ncol(testdata))])

    #transform values by scaling to original form
    c$net.result <- c$net.result * sm2 + sm1
    testdata$PredictedSales <- as.numeric(c$net.result)
    testdata$Sales <- testdata$Sales * sm2 + sm1

    if(plots){
        dev.new(width=18, height=10)
        testdata <- testdata[order(testdata$Date), ]
        #plot observed and predicted sales of test data
        plot(testdata$Date,testdata$Sales,type="h",xlab="Date",ylab="Sales",col='red',main=paste("Sales of store ",StoreID),xaxp=c(min(testdata$Date),max(testdata$Date),5),lwd=1)
        lines(testdata$Date,testdata$PredictedSales,type="p",col='blue',lwd=1.5)
        legend('topleft',legend=c("Observed","Predicted (Neural Network)"),col=c('red','blue'),cex=0.8,pch=c(20,21),lwd=1.5) 
    }
  
    # Store results in csv files
    Sales <- numeric(0)
    PredictedSales <- numeric(0)
    submission <- data.frame(Sales, PredictedSales)
    submission.tmp <- testdata[, c("Sales","PredictedSales")]
    submission <- rbind(submission, submission.tmp)
    write.table(submission, "./Rossmann Data/NNpredictedsales.csv", sep = ",", row.names = FALSE)

    #calculate the root mean square error value to check the accuracy of the model
    err <- RMSE(testdata$Sales,testdata$PredictedSales,type='NRMSE_SD')
    err
}

#Function to calculate RMSE for all stores and compute average RMSE for the model 
totalRMSENN <- function(){
    num <- length(train.list)
    total <- 0

    # Set a null data frame to store results
    Id <- integer(0)
    RMSE <- numeric(0)
    submission <- data.frame(Id=Id, NRMSE=RMSE)

    for(i in 1:num){
        err <- storeNN(i,plots=FALSE)
        print(c(i,err))
        submission <- rbind(submission, data.frame(Id=i,NRMSE=err))
        total <- total+err
    }
    #save NRMSE for each store in csv file
    write.table(submission, "./Rossmann Data/NNnrmse.csv", sep = ",", row.names = FALSE)
    print(total/num)
}
