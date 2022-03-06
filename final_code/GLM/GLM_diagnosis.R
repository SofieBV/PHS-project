#-----------------------------------------------

library(readr)

data <- read.csv('../data/weekdata.csv', header = TRUE) 
data <- as.data.frame (data)

# if we want to do it for a specific cancer type
#data <- subset(data, CancerType=='Lung')

logE <- log(data$PopSize)# -> add for population size

family1 = "poisson"


#--------- Introduce HB, cancer type,  age and sex as categorical variables #--------- 

data$HB <- as.factor( data$HB )

data$CancerType <- as.factor( data$CancerType )

data$Age <- as.factor( data$`Age Group`)
data$Sex <- as.factor( data$Sex )
levels(data$HB) 

levels(data$CancerType) 

levels(data$Age) 
levels(data$Sex) 


#--------- log-link is chosen by default in Poisson distribution. #--------- 
#build glm

# most complex
mod.1 <- glm( Count ~  offset(logLE) + HB + Date  + Sex + CancerType +Age + Pandemic_cat + JustPandemic , data = data, family=family1 )

summary(mod.1)

coef(mod.1)

mod.1.predict <- predict( mod.1, type = "response" ) # to generate estimated number of referrals

AIC(mod.1)

BIC(mod.1)

#--------- Let's try to make a plot of all the coefficients #--------- 

region_coef <- coef(mod.1)[2:14]
region_coef['HBS08000015'] <- 0
region_coef <- region_coef[order(region_coef)]

y_reg <- seq(length(region_coef))

par(mar=c(6.1,7,4.1,2.1))

plot(region_coef, y_reg,
     main="Coefficients for regions,
     pch=19, col='green', yaxt='n',
     xlab='', ylab='')
axis(2, at=y_reg, labels=names(region_coef), las=2)

