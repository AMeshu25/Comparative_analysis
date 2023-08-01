install.packages ('lme4')
install.packages ('MuMIn')
install.packages("strucchange")
install.packages("strucchange")
install.packages('sjPlot')
install.packages('MASS')
install.packages("caret")
library(lme4)
library(strucchange)
library(MuMIn)
library(sjPlot)
library(MASS)
library(glm2)
library(caret)
library(ggplot2)
library(stats)
library(stringr)



folder_path<- "C:\\Users\\TEMP.NAAMA\\PycharmProjects\\cameraAnalysis\\Rstudio\\CSV\\"
file_list <- list.files(folder_path)
models_data <- data.frame(name = character(),coef. = numeric(), std = numeric(), z = numeric(), 
                                pvalue = numeric(), r_mar = numeric(), r_con = numeric()) #prepare dataFrame

for(file in file_list){
  # Read the CSV file into a dataframe
  print(file)
  filePath <- paste0(folder_path,file) 
  feature_data<-read.csv(filePath,header=TRUE)  
  print(feature_data)
  col<-colnames(feature_data)
  camera_list<-c('MediaPipe', 'Nuitrack', 'ZED2mm', 'ZED4mm')
  for (c in camera_list) {
    c<-MediaPipe
    model<-glmer( paste0(c,_Vicon) ~ log(c)+(1|paste0(c,_subject)),family='poisson', data = feature_data )
    coef0 <- coef(model)
    coef1 <-  coef(model)['yellow_light_speed']
  
    
  }
  
  }

#---------------------------------handMovments------------------------------
handMovments<-read.csv("file.choose()",header = T)
colnames(handMovments)

#MediaPipe
model_hands_MediaPipe<-glmer(MediaPipe_Vicon~ log(MediaPipe)+(1|MediaPipe_subject),family='poisson', data = handMovments )
summary(model_hands_MediaPipe)
r.squaredGLMM(model_hands_MediaPipe) 
tab_model(model_hands_MediaPipe)

#ZED2mm
model_hands_ZED2mm<-glmer(ZED2mm_Vicon~ log(ZED2mm)+(1|ZED2mm_subject),family='poisson', data = handMovments )
summary(model_hands_ZED2mm)
r.squaredGLMM(model_hands_ZED2mm) 
tab_model(model_hands_ZED2mm)

#ZED4mm
model_hands_ZED4mm<-glmer(ZED4mm_Vicon~ log(ZED4mm)+(1|ZED4mm_subject),family='poisson', data = handMovments )
summary(model_hands_ZED4mm)
r.squaredGLMM(model_hands_ZED4mm) 

#Nuitrck
model_hands_Nuitrack<-glmer(Nuitrack_Vicon~ log(Nuitrack)+(1|ZED4mm_subject),family='poisson', data = handMovments )
summary(model_hands_Nuitrack)
r.squaredGLMM(model_hands_Nuitrack)




#---------------------------------DIFFRENCES------------------------------

difference<-read.csv(file.choose(),header = T)

#---------------------------------Nuitrack------------------------------
model_difference_Nuitrack<-lmer(L_x_Vicon_Nuitrack~ L_x_Nuitrack+(1|Nuitrack_subject), data = difference )
summary(model_difference_Nuitrack)
tab_model(model_difference_Nuitrack)

#Residuals check and linearity check
Predicted <- fitted(model_difference_Nuitrack)
unstdResiduals <- residuals(model_difference_Nuitrack)
stdResiduals <- (unstdResiduals) / sd(unstdResiduals)
plot(Predicted, stdResiduals, main = "Residuals vs. Fitted Plot", xlab = "Fitted Values", ylab = "Standardized Residuals")
abline(0,0,col="purple")

#normal check
#Q-Q Plot
model_difference_Nuitrack_res<-resid(model_difference_Nuitrack)
qqnorm(model_difference_Nuitrack_res,datax = FALSE)
qqline(model_difference_Nuitrack_res,datax = FALSE,col="purple")

hist(stdResiduals, prob=TRUE, main='Standardized residuals',ylim=c(0,0.55), xlab='Standardized residuals' )
lines(density(stdResiduals), col="purple", lwd=2)

#ks test for normal distribution
ks.test(x= stdResiduals,y="pnorm",alternative ="two.sided", exact = NULL)
shapiro.test(x= stdResiduals)

#BoxCox
boxcox(lm(L_x_Vicon_Nuitrack~ L_x_Nuitrack, data = difference ))


#---------------------------------diffrent try------------------------------
#---------------------------------handMovments------------------------------
handMovments<-read.csv(file.choose(),header = T)
colnames(handMovments)

model_hands<-glmer(Vicon~ cameraData*factor(cameraKind)+(1|subject),family='poisson',data = handMovments)
summary(model_hands)
tab_model(model_hands)

#---------------------------------difference------------------------------
difference<-read.csv(file.choose(),header = T)
colnames(difference)

difference_L_x<-lmer(L_x_Vicon~ L_x*factor(cameraKind)+(1|subjects),data = difference)
summary(difference_L_x)
tab_model(difference_L_x)

difference_L_y<-lmer(L_y_Vicon~ L_y*factor(cameraKind)+(1|subjects),data = difference)
summary(difference_L_y)
tab_model(difference_L_y)

