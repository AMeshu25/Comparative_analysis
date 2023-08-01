install.packages ('lme4')
install.packages ('MuMIn')
install.packages("strucchange")
install.packages("strucchange")
install.packages('sjPlot')
install.packages('MASS')
install.packages("caret")
install.packages('aod')
library(aod)
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
library(arm)



folder_path<- "C:\\Users\\TEMP.NAAMA\\PycharmProjects\\cameraAnalysis\\Rstudio\\CSV\\"
file_list <- list.files(folder_path)
models_data <- data.frame() #prepare dataFrame

for(file in file_list){
  # Read the CSV file into a dataframe
  feature<-substr(file,1,nchar(file)-4)
  print(file)
  filePath <- paste0(folder_path,file) 
  feature_data<-read.csv(filePath,header=TRUE)
  
  #MediaPipe
  model_MediaPipe<-glmer(MediaPipe_Vicon~ log(MediaPipe)+(1|MediaPipe_subject),family='poisson', data = feature_data )
  summary(model_MediaPipe)
  modelCoef<-coefTable(model_MediaPipe)[2]
  modelstd<-coefTable(model_MediaPipe)[4]
  chi<-((modelCoef-1)/modelstd)^2
  pvalue<-1-pchisq(chi,1)
  temp<-c(paste0(feature,"_MediaPipe") ,coefTable(model_MediaPipe)[2], pvalue)
  temp<-append(temp,r.squaredGLMM(model_MediaPipe)[1,])
  models_data<-rbind(models_data,temp )
  
  #ZED2mm
  model_ZED2mm<-glmer(ZED2mm_Vicon~ log(ZED2mm)+(1|ZED2mm_subject),family='poisson', data = feature_data )
  summary(model_ZED2mm)
  modelCoef<-coefTable(model_ZED2mm)[2]
  modelstd<-coefTable(model_ZED2mm)[4]
  chi<-((modelCoef-1)/modelstd)^2
  pvalue<-1-pchisq(chi,1)
  temp<-c(paste0(feature,"_ZED2mm") ,coefTable(model_ZED2mm)[2], pvalue)
  temp<-append(temp,r.squaredGLMM(model_ZED2mm)[1,])
  models_data<-rbind(models_data,temp )
  
  #ZED4mm
  model_ZED4mm<-glmer(ZED4mm_Vicon~ log(ZED4mm)+(1|ZED4mm_subject),family='poisson', data = feature_data )
  summary(model_ZED4mm)
  modelCoef<-coefTable(model_ZED4mm)[2]
  modelstd<-coefTable(model_ZED4mm)[4]
  chi<-((modelCoef-1)/modelstd)^2
  pvalue<-1-pchisq(chi,1)
  temp<-c(paste0(feature,"_ZED4mm") ,coefTable(model_ZED4mm)[2], pvalue)
  temp<-append(temp,r.squaredGLMM(model_ZED4mm)[1,])
  models_data<-rbind(models_data,temp )
  
  #Nuitrck
  model_Nuitrack<-glmer(Nuitrack_Vicon~ log(Nuitrack)+(1|ZED4mm_subject),family='poisson', data = feature_data )
  summary(model_Nuitrack)
  modelCoef<-coefTable(model_Nuitrack)[2]
  modelstd<-coefTable(model_Nuitrack)[4]
  chi<-((modelCoef-1)/modelstd)^2
  pvalue<-1-pchisq(chi,1)
  temp<-c(paste0(feature,"_Nuitrack") ,coefTable(model_Nuitrack)[2], pvalue)
  temp<-append(temp,r.squaredGLMM(model_Nuitrack)[1,])
  models_data<-rbind(models_data,temp )
  
}
folder_path_new<- "C:\\Users\\TEMP.NAAMA\\PycharmProjects\\cameraAnalysis\\Rstudio\\Results\\"
write.csv(models_data, filePath <- paste0(folder_path_new,"PoissonWald.csv") , row.names = FALSE)

  


#---------------------------------handMovments------------------------------
handMovments<-read.csv(paste0(folder_path,'handsmovment.csv') ,header = T)
colnames(handMovments)

#MediaPipe
model_hands_MediaPipe<-glmer(MediaPipe_Vicon~ log(MediaPipe)+(1|MediaPipe_subject),family='poisson', data = handMovments )
summary(model_hands_MediaPipe)
modelCoef<-coefTable(model_hands_MediaPipe)[2]
modelstd<-coefTable(model_hands_MediaPipe)[4]
wald.test(b=modelCoef,Sigma=modelstd, H0=c(1), Terms = 1)  
temp<-c('model_hands_MediaPipe',coefTable(model_hands_MediaPipe)[2])
temp<-append(temp, )
models_data<-rbind(models_data,temp )


#ZED2mm
model_hands_ZED2mm<-glmer(ZED2mm_Vicon~ log(ZED2mm)+(1|ZED2mm_subject),family='poisson', data = handMovments )
summary(model_hands_ZED2mm)
modelCoef<-coefTable(model_hands_ZED2mm)[2]
modelstd<-coefTable(model_hands_ZED2mm)[4]
wald.test(b=modelCoef,Sigma=modelstd, H0=c(1), Terms = 1)  
temp<-c('model_hands_ZED2mm',0.2109)
temp<-append(temp,r.squaredGLMM(model_hands_ZED2mm)[1,])
models_data<-rbind(models_data,temp )

#ZED4mm
model_hands_ZED4mm<-glmer(ZED4mm_Vicon~ log(ZED4mm)+(1|ZED4mm_subject),family='poisson', data = handMovments )
summary(model_hands_ZED4mm)
temp<-c('model_hands_ZED4mm',-0.07318)
temp<-append(temp,r.squaredGLMM(model_hands_ZED4mm)[1,])
models_data<-rbind(models_data,temp ) 

#Nuitrck
model_hands_Nuitrack<-lmer(Nuitrack_Vicon~ Nuitrack+(1|Nuitrack_subject), data = handMovments )
summary(model_hands_Nuitrack)
modelCoef<-coefTable(model_hands_Nuitrack)[2]
modelstd<-0.399
chi<-((modelCoef-1)/modelstd)^2
pvalue<-1-pchisq(chi,1)
  
temp<-c('model_hands_Nuitrack',0.8917)
temp<-append(temp,r.squaredGLMM(model_hands_Nuitrack)[1,])
models_data<-rbind(models_data,temp ) 


