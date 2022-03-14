
library(readr)
library(ggplot2)
data <- read.csv('../data/weekdata.csv')
#data <- read.csv("~/Desktop/NHS Project/PHS-project-main/final_code/data/weekdata_old.csv")
data <- as.data.frame (data)

# if we want to do it for a specific cancer type
data <- subset(data, CancerType=='Colorectal')  # 'Breast', Lung'

logE <- log(data$PopSize)# -> add for population size

family1 = "poisson"


#--------- Introduce HB, cancer type,  age and sex as categorical variables #--------- 

data$HB <- as.factor( data$HB )


data$Age <- as.factor( data$Age.Group)
data$Sex <- as.factor( data$Sex )
levels(data$HB) 


levels(data$Age) 
levels(data$Sex) 

levels(data$CancerType) 


#--------- log-link is chosen by default in Poisson distribution. #--------- 
#build glm

# most complex



mod.1 <- glm( Count ~  offset(logE) + HB + Date +Age+ + Sex + JustPandemic + Pandemic_cat, data = data, family=family1 ) # sex not in breast

summary(mod.1)

coef(mod.1)

mod.1.predict <- predict( mod.1, type = "response" ) # to generate estimated number of referrals

AIC(mod.1)

BIC(mod.1)

#--------- Extending the data by adding two new columns which show fitted data

data <- cbind( data, mod.1.predict/data$PopSize )
#data <- cbind( data, mod.1.predict )

names(data)[14] <- c("fitted")

data$rates <- data$Count/ data$PopSize



#--------- Let's try to make a plot of all the coefficients #--------- 
region_coef <- coef(mod.1)[2:14]
region_coef['HBS08000015'] <- 0
region_coef <- region_coef[order(region_coef)]

y_reg <- seq(length(region_coef))

par(mar=c(6.1,7,4.1,2.1))

plot(region_coef, y_reg,
     main="Coefficients for regions for Breast cancer",
     pch=19, col='green', yaxt='n',
     xlab='', ylab='')
axis(2, at=y_reg, labels=names(region_coef), las=2)



#age

age_coef <- coef(mod.1)[16:17]
age_coef['Age 0-49'] <- 0
age_coef <- age_coef[order(age_coef)]

y_age <- seq(length(age_coef))

par(mar=c(6.1,7,4.1,2.1))

plot(age_coef, y_age,
     main="Coefficients for age for Breast cancer",
     pch=19, col='green', yaxt='n',
     xlab='', ylab='')
axis(2, at=y_age, labels=names(age_coef), las=2)





#sex

sex_coef <- coef(mod.1)[18]
sex_coef['SexFemale']<- 0
sex_coef <- sex_coef[order(sex_coef)]

y_sex <- seq(length(sex_coef))

par(mar=c(6.1,7,4.1,2.1))

plot(sex_coef, y_sex,
     main="Coefficients for age for Breast cancer",
     pch=19, col='green', yaxt='n',
     xlab='', ylab='')
axis(2, at=y_sex, labels=names(sex_coef), las=2)

