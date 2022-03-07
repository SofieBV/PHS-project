library(ggplot2)

#-----------------------------------------------

data <- read.csv('../data/31days.csv', header = TRUE) 

data2 <- read.csv("../data/62days.csv", header = TRUE) 

data <- as.data.frame (data2)

logLE <- log(data$PopSize)# -> add for population size

family1 = "poisson"


#--------- Introduce region (HB) and cancer type as categorical variables #--------- 

data$HB <- as.factor( data$HB )

data$CancerType <- as.factor( data$CancerType )

levels(data$HB) 

levels(data$CancerType) 

data$DateSquared <- (data$Date)^2

#--------- log-link is chosen by default in Poisson distribution. #--------- 

mod.1 <- glm( NumberOfEligibleReferrals62DayStandard ~  offset(logLE) + HB + CancerType +Date:CancerType + Date +
                Pandemic + PandemicRecovery, data = data, family=family1 )

summary(mod.1)

coef(mod.1)

mod.1.predict <- predict( mod.1, type = "response" ) # to generate estimated number of referrals

AIC(mod.1)

BIC(mod.1)

ci <- confint(mod.1)
ci

results <- summary(mod.1)$coefficients
results <- cbind(results, '2.5%'=ci[,1])
results <- cbind(results, '97.5%'=ci[,2])
results <- cbind(results, 'AIC'=AIC(mod.1))
results <- cbind(results, 'BIC'=BIC(mod.1))
write.csv(results,"results/62_eligible_Pop_Time_Pan_Rec_HB_CT.csv")

#--------- Extending the data by adding two new columns which show fitted data

data <- cbind( data, 'fitted'=mod.1.predict/data$PopSize )
#data <- cbind( data, mod.1.predict )

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

region_names <- c('NHS Borders','NHS Dumfries and Galloway','NHS Forth Valley','NHS Grampian',
                           'NHS Highland','NHS Lothian','NHS Orkney','NHS Shetland','NHS Western Isles','NHS Fife','NHS Tayside',
                           'NHS Greater Glasgow and Clyde','NHS Lanarkshire','NHS Ayrshire and Arran')
region_coef <- coef(mod.1)[2:14]
region_coef['HBS08000015'] <- 0
region_ci_min <- ci[2:14,1]
region_ci_max <- ci[2:14,2]
region_ci_min['HBS08000015'] <- 0
region_ci_max['HBS08000015'] <- 0
region_ci_min <- region_ci_min[order(region_coef)]
region_ci_max <- region_ci_max[order(region_coef)]
region_names <- region_names[order(region_coef)]
region_coef <- region_coef[order(region_coef)]

cancer_coef <- coef(mod.1)[15:23]
cancer_coef['CancerTypeBreast'] <- 0
cancer_ci_min <- ci[15:23,1]
cancer_ci_max <- ci[15:23,2]
cancer_ci_min['CancerTypeBreast'] <- 0
cancer_ci_max['CancerTypeBreast'] <- 0
cancer_ci_min <- cancer_ci_min[order(cancer_coef)]
cancer_ci_max <- cancer_ci_max[order(cancer_coef)]
cancer_coef <- cancer_coef[order(cancer_coef)]

y_reg <- seq(length(region_coef))
y_can <- seq(length(cancer_coef))

df_reg <- data.frame(region_coef, y_reg, region_ci_min, region_ci_max)
df_can <- data.frame(cancer_coef, y_can, cancer_ci_min, cancer_ci_max)

png(file="results/62_eligible_Pop_Time_Pan_Rec_HB_CT_reg.png",
    width=600, height=350)
plt <- ggplot(data = df_reg ,aes(x=region_coef, y=y_reg)) + 
  geom_point() + 
  geom_errorbarh(aes(xmin=region_ci_min, xmax=region_ci_max))
plt + ggtitle("Coefficients for regions") +
  xlab("") + ylab("") + 
  scale_y_continuous(breaks = y_reg, labels = region_names)
dev.off()

png(file="results/62_eligible_Pop_Time_Pan_Rec_HB_CT_can.png",
    width=600, height=350)
plt <- ggplot(data = df_can ,aes(x=cancer_coef, y=y_can)) + 
  geom_point() + 
  geom_errorbarh(aes(xmin=cancer_ci_min, xmax=cancer_ci_max))
plt + ggtitle("Coefficients for cancer types") +
  xlab("") + ylab("") + 
  scale_y_continuous(breaks = y_can, labels = sub('CancerType','',names(cancer_coef)))
dev.off()

