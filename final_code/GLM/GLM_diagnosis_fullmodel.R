
library(readr)
library(ggplot2)

data <- read.csv('../data/weekdata.csv')
#data <- read.csv("~/Desktop/NHS Project/PHS-project-main/final_code/data/weekdata_old.csv")
data <- as.data.frame (data)

# if we want to do it for a specific cancer type
#data <- subset(data, CancerType=='Breast')

logLE <- log(data$PopSize)# -> add for population size

family1 = "poisson"


#--------- Introduce HB, cancer type,  age and sex as categorical variables #--------- 

data$HB <- as.factor( data$HB )

data$CancerType <- as.factor( data$CancerType )

data$Age <- as.factor( data$Age.Group)
data$Sex <- as.factor( data$Sex )
levels(data$HB) 

levels(data$CancerType) 

levels(data$Age) 
levels(data$Sex) 


#--------- log-link is chosen by default in Poisson distribution. #--------- 
#build glm

# most complex


mod.1 <- glm( Count ~  offset(logLE) +Date + Pandemic_cat  + JustPandemic, data = data, family=family1 )

summary(mod.1)

coef(mod.1)

mod.1.predict <- predict( mod.1, type = "response" ) # to generate estimated number of referrals

AIC(mod.1)

BIC(mod.1)



mod.2 <- glm( Count ~  offset(logLE)  +Age+ Date + CancerType+ HB+ Sex , data = data, family=family1 )


summary(mod.2)

coef(mod.2)

mod.2.predict <- predict( mod.2, type = "response" ) # to generate estimated number of referrals

AIC(mod.2)

BIC(mod.2)






mod.3 <- glm( Count ~  offset(logLE) + HB + Date + CancerType + Sex , data = data, family=family1 )

summary(mod.3)

coef(mod.3)

mod.3.predict <- predict( mod.3, type = "response" ) # to generate estimated number of referrals

AIC(mod.3)

BIC(mod.3)



mod.4 <- glm( Count ~  offset(logLE) + HB + Date + CancerType + Sex + Age , data = data, family=family1 )

summary(mod.4)

coef(mod.4)

mod.4.predict <- predict( mod.4, type = "response" ) # to generate estimated number of referrals

AIC(mod.4)

BIC(mod.4)




mod.5 <- glm( Count ~  offset(logLE) + HB + Date + CancerType + Age + Pandemic_cat, data = data, family=family1 )

summary(mod.5)

coef(mod.5)

mod.5.predict <- predict( mod.5, type = "response" ) # to generate estimated number of referrals

AIC(mod.5)

BIC(mod.5)



# ,model with best bic
mod.1 <- glm( Count ~  offset(logLE) +  Date + HB+ CancerType + Sex+Age + Pandemic_cat + JustPandemic, data = data, family=family1 )

summary(mod.1)

coef(mod.1)

mod.1.predict <- predict( mod.1, type = "response" ) # to generate estimated number of referrals

AIC(mod.1)

BIC(mod.1)

#--------- Let's try to make a plot of all the coefficients #--------- 

ci <- confint(mod.1)
ci

results <- summary(mod.1)$coefficients
results <- cbind(results, '2.5%'=ci[,1])
results <- cbind(results, '97.5%'=ci[,2])
results <- cbind(results, 'AIC'=AIC(mod.1))
results <- cbind(results, 'BIC'=BIC(mod.1))
write.csv(results,"Desktop/PHS-project-main2/final_code/GLM/fullmodel.csv")

#--------- Extending the data by adding two new columns which show fitted data

data <- cbind( data, 'fitted'=mod.1.predict/data$PopSize )
#data <- cbind( data, mod.1.predict )

data$rates <- data$Count / data$PopSize

#--------- Let's try to make a plot showing fitted data #--------- 

data_plot <- subset(subset(data, HB=='S08000015'), CancerType=='Breast')

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
region_coef <- coef(mod.1)[3:15]
region_coef['HBS08000015'] <- 0
region_ci_min <- ci[3:15,1]
region_ci_max <- ci[3:15,2]
region_ci_min['HBS08000015'] <- 0
region_ci_max['HBS08000015'] <- 0
region_ci_min <- region_ci_min[order(region_coef)]
region_ci_max <- region_ci_max[order(region_coef)]
region_names <- region_names[order(region_coef)]
region_coef <- region_coef[order(region_coef)]

cancer_coef <- coef(mod.1)[16:44]
cancer_coef['CancerTypeNeoplasm'] <- 0
cancer_ci_min <- ci[16:44,1]
cancer_ci_max <- ci[16:44,2]
cancer_ci_min['CancerTypeNeoplasm'] <- 0
cancer_ci_max['CancerTypeNeoplasm'] <- 0
cancer_ci_min <- cancer_ci_min[order(cancer_coef)]
cancer_ci_max <- cancer_ci_max[order(cancer_coef)]
cancer_coef <- cancer_coef[order(cancer_coef)]


sex_coef <- coef(mod.1)[45]
sex_coef['SexFemale'] <- 0
sex_ci_min <- ci[45,1]
sex_ci_max <- ci[45,2]
sex_ci_min['SexFemale'] <- 0
sex_ci_max['SexFemale'] <- 0
sex_ci_min <- sex_ci_min[order(sex_coef)]
sex_ci_max <- sex_ci_max[order(sex_coef)]
sex_coef <- sex_coef[order(sex_coef)]


##
age_coef <- coef(mod.1)[46:47]
age_coef['0-49'] <- 0
age_ci_min <- ci[46:47,1]
age_ci_max <- ci[46:47,2]
age_ci_min['0-49'] <- 0
age_ci_max['0-49'] <- 0
age_ci_min <- age_ci_min[order(age_coef)]
age_ci_max <- age_ci_max[order(age_coef)]
age_coef <- age_coef[order(age_coef)]



y_reg <- seq(length(region_coef))
y_can <- seq(length(cancer_coef))
y_sex <- seq(length(sex_coef))
y_age <- seq(length(age_coef))



df_reg <- data.frame(region_coef, y_reg, region_ci_min, region_ci_max)
df_can <- data.frame(cancer_coef, y_can, cancer_ci_min, cancer_ci_max)
df_sex <- data.frame(sex_coef, y_sex, sex_ci_min, sex_ci_max)
df_age <- data.frame(age_coef, y_age, age_ci_min, age_ci_max)

png(file="Desktop/PHS-project-main2/final_code/GLM/coeffs_reg.png",
    width=600, height=350)
plt <- ggplot(data = df_reg ,aes(x=region_coef, y=y_reg)) + 
  geom_point() + 
  geom_errorbarh(aes(xmin=region_ci_min, xmax=region_ci_max))
plt + ggtitle("Coefficients for regions") +
  xlab("") + ylab("") + 
  scale_y_continuous(breaks = y_reg, labels = region_names)
dev.off()




png(file="Desktop/PHS-project-main2/final_code/GLM/coeffs_ct.png",
    width=600, height=350)
plt <- ggplot(data = df_can ,aes(x=cancer_coef, y=y_can)) + 
  geom_point() + 
  geom_errorbarh(aes(xmin=cancer_ci_min, xmax=cancer_ci_max))
plt + ggtitle("Coefficients for cancer types") +
  xlab("") + ylab("") + 
  scale_y_continuous(breaks = y_can, labels = sub('CancerType','',names(cancer_coef)))
dev.off()





png(file="Desktop/PHS-project-main2/final_code/GLM/coeffs_sex.png",
    width=600, height=350)
plt <- ggplot(data = df_sex,aes(x=sex_coef, y=y_sex)) + 
  geom_point() + 
  geom_errorbarh(aes(xmin=sex_ci_min, xmax=sex_ci_max))
plt + ggtitle("Coefficients for sex") +
  xlab("") + ylab("") + 
  scale_y_continuous(breaks = y_sex, labels = sub('Sex','',names(sex_coef)))
dev.off()





png(file="Desktop/PHS-project-main2/final_code/GLM/coeffs_age.png",
    width=600, height=350)
plt <- ggplot(data = df_age ,aes(x=age_coef, y=y_age)) + 
  geom_point() + 
  geom_errorbarh(aes(xmin=age_ci_min, xmax=age_ci_max))
plt + ggtitle("Coefficients for age groups") +
  xlab("") + ylab("") + 
  scale_y_continuous(breaks = y_age, labels = sub('Age.Group','',names(age_coef)))
dev.off()
