#convert numeric to factors
convertFieldsToFactors <- function(data){
    data$SchoolHoliday <- as.factor(data$SchoolHoliday)
    data$Promo <- as.factor(data$Promo)
    data$Open <- as.factor(data$Open)
    data$Store <- as.factor(data$Store)
    data
}

#read the training data
train <- read.csv("./Rossmann Data/train.csv")

#convert fields to factors
train <- convertFieldsToFactors(train)

#convert Date field into Date format 
train$Date <- as.Date(train$Date)

#order training data based on Date
train <- train[order(train$Date), ]

#add new columns
train$DateMonth <- as.numeric(strftime(train$Date, format="%m"))
train$DateDay <- as.numeric(strftime(train$Date, format="%d"))
train$DateYear <- as.numeric(strftime(train$Date, format="%y"))

#drop the rows when store was closed
train <- train[which(train$Open==1),]

#group train data based on Store ID
train.list <- split(train, as.factor(train$Store))

