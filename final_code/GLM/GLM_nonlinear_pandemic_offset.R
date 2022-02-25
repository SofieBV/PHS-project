#-----------------------------------------------

data <- read.csv('../data/62days.csv', header = TRUE) 

data2 <- read.csv("../data/31days.csv", header = TRUE) 

data <- as.data.frame (data)

logLE <- log(data$PopSize)# -> add for population size

family1 = "poisson"


#--------- Introduce region (HB) and cancer type as categorical variables #--------- 

data$HB <- as.factor( data$HB )

data$CancerType <- as.factor( data$CancerType )

levels(data$HB) 

levels(data$CancerType) 

#--------- log-link is chosen by default in Poisson distribution. #--------- 

mod.1 <- glm( NumberOfEligibleReferrals62DayStandard ~  offset(logLE) + HB + CancerType + Date + JustPandemic + Pandemic_cat, data = data, family=family1 )

summary(mod.1)

coef(mod.1)

mod.1.predict <- predict( mod.1, type = "response" ) # to generate estimated number of referrals

AIC(mod.1)

BIC(mod.1)

#--------- Extending the data by adding two new columns which show fitted data

data <- cbind( data, mod.1.predict/data$PopSize )
#data <- cbind( data, mod.1.predict )

names(data)[14] <- c("fitted")

data$rates <- data$NumberOfEligibleReferrals62DayStandard / data$PopSize

#--------- Let's try to make a plot showing fitted data #--------- 

data_plot <- subset(subset(data, HB=='S08000024'), CancerType=='Breast')

plot(data_plot$Date, data_plot$rates,
     main="Nr of Referrals in NHS Lothian for Breast Cancer",
     ylab="nr of referrals", xlab='time',
     type="l",
     col="blue", xaxt='n') 
axis(1, at=data_plot$Date, labels=data_plot$Quarter)
lines(data_plot$Date, data_plot$fitted, col='red')
legend("topleft",
       c("actual","fitted"),
       fill=c("blue","red"))
#--------- Let's try to make a plot of all the coefficients #--------- 

region_coef <- coef(mod.1)[2:14]
region_coef['HBS08000015'] <- 0
region_coef <- region_coef[order(region_coef)]


cancer_coef <- coef(mod.1)[15:23]
cancer_coef['CancerTypeBreast'] <- 0
cancer_coef <- cancer_coef[order(cancer_coef)]

y_reg <- seq(length(region_coef))
y_can <- seq(length(cancer_coef))

par(mar=c(6.1,7,4.1,2.1))

plot(region_coef, y_reg,
  main="Coefficients for regions",
  pch=19, col='green', yaxt='n',
  xlab='', ylab='')
axis(2, at=y_reg, labels=names(region_coef), las=2)

plot(cancer_coef, y_can,
     main="Coefficients for cancer types",
     pch=19, col='green', yaxt='n',
     xlab='', ylab='')
axis(2, at=y_can, labels=names(cancer_coef), las=2)

