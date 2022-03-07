library(ggplot2)

#-----------------------------------------------

data <- read.csv('../data/31days.csv', header = TRUE) 

data2 <- read.csv("../data/62days.csv", header = TRUE) 

data <- as.data.frame (data)

t <- c('NCA','NCA', 'NCA', 'NCA', 'NCA', 'NCA', 'SCAN','SCAN','SCAN','SCAN', 'WOSCAN','WOSCAN','WOSCAN','WOSCAN')
f <- c('S08000020','S08000022', 'S08000025', 'S08000026', 'S08000030', 'S08000028', 'S08000016','S08000017',
       'S08000029','S08000024', 'S08000015','S08000019','S08000031','S08000032')

data$HB <- mapvalues(data$HB,f,t)

data_new <- aggregate(cbind(NumberOfEligibleReferrals31DayStandard=data$NumberOfEligibleReferrals31DayStandard,
                            NumberOfEligibleReferralsTreatedWithin31Days=data$NumberOfEligibleReferralsTreatedWithin31Days,
                            PopSize = data$PopSize), 
                      by=list( Quarter = data$Quarter, Date=data$Date,
                               Pandemic=data$Pandemic, JustPandemic=data$JustPandemic, Pandemic_cat=data$Pandemic_cat), FUN=sum)

data <- data_new

logLE <- log(data$PopSize)# -> add for population size

family1 = "poisson"

data$DateSquared <- (data$Date)^2

#--------- log-link is chosen by default in Poisson distribution. #--------- 

mod.1 <- glm( NumberOfEligibleReferrals31DayStandard ~  offset(logLE) + Date  , data = data, family=family1 )
mod.2 <- glm( NumberOfEligibleReferrals31DayStandard ~  offset(logLE) + Date +DateSquared , data = data, family=family1 )
mod.3 <- glm( NumberOfEligibleReferrals31DayStandard ~  offset(logLE) + Date +JustPandemic , data = data, family=family1 )
mod.4 <- glm( NumberOfEligibleReferrals31DayStandard ~  offset(logLE) + Date +DateSquared + JustPandemic , data = data, family=family1 )
mod.5 <- glm( NumberOfEligibleReferrals31DayStandard ~  offset(logLE) + Date +Pandemic_cat + JustPandemic , data = data, family=family1 )
mod.6 <- glm( NumberOfEligibleReferrals31DayStandard ~  offset(logLE) + Date +DateSquared +Pandemic_cat+ JustPandemic , data = data, family=family1 )

summary(mod.1)
confint(mod.1)
BIC(mod.1)
summary(mod.2)
confint(mod.2)
BIC(mod.2)
summary(mod.3)
confint(mod.3)
BIC(mod.3)
summary(mod.4)
confint(mod.4)
BIC(mod.4)
summary(mod.5)
confint(mod.5)
BIC(mod.5)
summary(mod.6)
confint(mod.6)
BIC(mod.6)

summary(mod.1)

coef(mod.1)

mod.1.predict <- predict( mod.1, type = "response" ) # to generate estimated number of referrals
mod.2.predict <- predict( mod.2, type = "response" ) # to generate estimated number of referrals
mod.3.predict <- predict( mod.3, type = "response" ) # to generate estimated number of referrals
mod.4.predict <- predict( mod.4, type = "response" ) # to generate estimated number of referrals

AIC(mod.1)

BIC(mod.1)

ci <- confint(mod.1)
ci

results <- summary(mod.1)$coefficients
results <- cbind(results, '2.5%'=ci[,1])
results <- cbind(results, '97.5%'=ci[,2])
results <- cbind(results, 'AIC'=AIC(mod.1))
results <- cbind(results, 'BIC'=BIC(mod.1))
write.csv(results,"results/62_eligible_ALL_ALL_Pop_Time_Pan.csv")

#--------- Extending the data by adding two new columns which show fitted data

data <- cbind( data, 'fitted1'=mod.1.predict/data$PopSize )
data <- cbind( data, 'fitted2'=mod.2.predict/data$PopSize )
data <- cbind( data, 'fitted3'=mod.3.predict/data$PopSize )
data <- cbind( data, 'fitted4'=mod.4.predict/data$PopSize )
#data <- cbind( data, mod.1.predict )

data$rates <- data$NumberOfEligibleReferrals62DayStandard / data$PopSize

#--------- Let's try to make a plot showing fitted data #--------- 

data_plot <- data

png(file="results/62_eligible_ALL_together_plot.png",
    width=600, height=350)
plot(data_plot$Date, data_plot$rates,
     main="Nr of 62 day eligible referrals in Scotland for all cancer types",
     ylab="rate of referrals", xlab='time',
     type="l",
     col="black", xaxt='n') 
axis(1, at=data_plot$Date, labels=data_plot$Quarter)
lines(data_plot$Date, data_plot$fitted1, col='blue')
lines(data_plot$Date, data_plot$fitted2, col='red')
lines(data_plot$Date, data_plot$fitted3, col='orange')
lines(data_plot$Date, data_plot$fitted4, col='green')
legend("topleft",
       c("actual","fitted model 1", 'fitted model 2', 'fitted model 3', 'fitted model 4'),
       fill=c("black","blue",'red', 'orange','green'))
dev.off()

