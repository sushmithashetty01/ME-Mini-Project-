cat("\n--------------------------------------------------------------\n")
cat("Sales Forecasting using Time Series and Neural Network Models\n")
cat("\nSetting up data...\n")
source("setup.R")

cat("\nAnalysis...\n")
source("analysis.R")

source("arima.R")
source("neuralnet.R")
source("compare.R")

callArima <- function(){
	id <- readline(prompt="Enter store ID(1-1115): ")
	id <- as.integer(id)
	err <- storeArima(id)
	cat("\n--------------\nRMSE:",round(err,5),"\n--------------\n")
}

callNN <- function(){
	id <- readline(prompt="Enter store ID(1-1115): ")
	id <- as.integer(id)
	err <- storeNN(id)
	cat("\n--------------\nRMSE:",round(err,5),"\n--------------\n")
}

callCompare <- function(){
	id <- readline(prompt="Enter store ID(1-1115): ")
	id <- as.integer(id)
	compareModels(id)
}

callEnd <- function() {
	cat("Exited")
	cat("\n--------------------------------------------------------------\n")
}

while(TRUE){
	switch(menu(c("Arima","Neural Network","Compare models","Exit")),callArima(),callNN(),callCompare(),break)
}