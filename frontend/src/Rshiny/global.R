# library(DT)
# library(RColorBrewer)
# library(maps)
# library(mapproj)
# 
# library(vroom)
# library(reticulate)
library(shinyjs)
library(shiny)
library(shinymicrophone)
library(RCurl)
library(data.table)
library(httr)
library(stringr)
library(ggplot2)
library(dplyr)

# Define python and shiny path
path_python = "C:/Users/scofi/PycharmProjects/app/Scripts/python.exe"
path_shiny = "C:/Users/scofi/PycharmProjects/app"


# file size maximun 50 Mb
options(shiny.maxRequestSize = 50 * 1024^2)

# Define any Python packages needed for the app here:
PYTHON_DEPENDENCIES = c('pip', 'numpy','speech_recognition','pyaudio','os')

emoplot <- function(){
  emotion <- read.csv2( paste0(path_shiny,"/emotion/em_text.csv"),header=TRUE, sep=",")
  # Basic piechart
  ggplot(emotion, aes(x="", y=Score, fill=Emotion)) +
    geom_bar(stat="identity", width=1,color="white") +
    coord_polar("y", start=0) +
    theme_void() +
    scale_fill_manual("legend", values = c("anger" ="#df2c24","disgust"="#844421","fear"="grey","happiness" ="orange","love" ="skyblue","sadness" ="#141414","surprise"="pink") )
  #scale_fill_manual("legend", values = c("anger" ="#df2c24","fear"="grey","happiness" ="orange","love" ="skyblue","sadness" ="#141414","surprise"="pink") )
}

# # source_python("C:/Users/KaichengLi/PycharmProjects/my_project/test.py")
# run_py <- function(python, rec_source, input_file){
#   system(
#     paste(
#       python, rec_source, input_file, sep=" "), intern=TRUE,show.output.on.console=T)
#   return(
#     print(vroom::vroom(paste0(path_shiny,"/python_file/output.txt"),delim = "."))
#     #print(vroom::vroom(paste0(path_shiny,"/Rshiny/output/output.txt"),delim = "."))
#     #print(read.table("output.txt",sep = "\t",as.is = F,strip.white = T))
#   )  
# }
# 
# # s2t_api_fr("C:/Users/KaichengLi/PycharmProjects/my_project/audio/fr_test_1.wav")
# s2t_api_en <- function(input_data_path){
#   run_py(
#     path_python,
#     "C:/Users/KaichengLi/PycharmProjects/my_project/python_file/s2t_api_doc_en.py",
#     input_data_path
#   )
# }
# 
# s2t_api_fr <- function(input_data_path){
#   run_py(
#     path_python,
#     "C:/Users/KaichengLi/PycharmProjects/my_project/python_file/s2t_api_doc_fr.py",
#     input_data_path
#   )
# }
# 
# s2t_loc_en <- function(input_data_path){
#   run_py(
#     path_python,
#     "C:/Users/KaichengLi/PycharmProjects/my_project/python_file/local_s2t_en.py",
#     input_data_path
#   )
# }
# 
# s2t_loc_fr <- function(input_data_path){
#   run_py(
#     path_python,
#     "C:/Users/KaichengLi/PycharmProjects/my_project/python_file/local_s2t_fr.py",
#     input_data_path
#   )
# }

##############################3
doc_api <- function(input_file,language){
  system(
    paste0('python -c',
           '"import os,speech2text;',
           'speech2text.api.api_doc.API_document(input_audio = \'',input_file,'\' ,language = \'',language,'\');',
           'em_audio = speech2text.emotion.emo.EmotionAudio( \'',input_file,'\').save_em_audio();',
           'em_text = speech2text.emotion.emo.EmotionText(\'',language,'\').save_em_text();',
           'speech2text.emotion.emo.final_emotion(em_text, em_audio)"')
  )
  return(print(vroom::vroom(paste0(path_shiny,"/Rshiny/output/output.txt"),delim = ".")))
}

# doc_api("C:/Users/scofi/PycharmProjects/app/audio/en_long.wav","EN")
# emoplot()

doc_loc <- function(input_file,language){
  system(
    paste0('python -c',
           '"import os,speech2text;',
           'speech2text.model.local.rec_doc(input_audio = \'',input_file,'\' ,language = \'',language,'\');',
           'em_audio = speech2text.emotion.emo.EmotionAudio( \'',input_file,'\').save_em_audio();',
           'em_text = speech2text.emotion.emo.EmotionText(\'',language,'\').save_em_text();',
           'speech2text.emotion.emo.final_emotion(em_text, em_audio)"')
  )
  return(print(vroom::vroom(paste0(path_shiny,"/Rshiny/output/output.txt"),delim = ".")))
}




#doc_api("C:/Users/KaichengLi/PycharmProjects/my_project/audio/fr_test_4.wav","FR")

# speech2text.model.local.rec_doc("C:\\Users\\KAICHE~1\\AppData\\Local\\Temp\\RtmpeAupxC/020414d02f1f22b76251177c/0.mp3","FR")




#add punctuation
# add_pun <- function(input_text){
#   system(paste(
#     path_python,
#     "C:/Users/KaichengLi/PycharmProjects/my_project/python_file/punctuation.py",
#     input_text, 
#     sep=" "), intern=TRUE,show.output.on.console=T)
#   return(
#     #print(vroom::vroom("output_punctuation.txt",delim = "."))
#     #print(read.table("output_punctuation.txt",header  = T,sep = "\t",as.is = F,strip.white = T))
#     print(data.table::fread("C:/Users/KaichengLi/PycharmProjects/my_project/python_file/output_punctuation.txt",sep = "\t",dec = "."))
#   )  
# }
############################################

#add punctuation
add_pun <- function(){
  system(paste0('python -c', 
                '"import os, speech2text;',
                'speech2text.punctuation.pun.PUN()"'))
  return(
    #print(vroom::vroom("output_punctuation.txt",delim = "."))
    #print(read.table("output_punctuation.txt",header  = T,sep = "\t",as.is = F,strip.white = T))
    print(data.table::fread(paste0(path_shiny,"/Rshiny/output/output_punctuation.txt"),sep = "\t",dec = "."))
  )  
}

#############################################

# micophone
mico_api <- function(language){
  system(
    paste0('python -c',
           '"import os, speech2text;',
           'speech2text.mico.mico_api.mico_API(language=\'',language,'\');',
           'em_audio = speech2text.emotion.emo.EmotionAudio(\'',path_shiny,'\' + \'"/Rshiny/www/micophone/audio.wav"\').save_em_audio();',
           'em_text = speech2text.emotion.emo.EmotionText(\'',language,'\').save_em_text();',
           'speech2text.emotion.emo.final_emotion(em_text, em_audio)"')
  )
  return(print(vroom::vroom(paste0(path_shiny,"/Rshiny/output/output.txt"),delim = ".")))
}

mico_loc <- function(language){
  system(
    paste0('python -c',
           '"import os, speech2text;',
           'speech2text.mico.mico_loc.mico_LOC(language=\'',language,'\');',
           'em_audio = speech2text.emotion.emo.EmotionAudio(\'',path_shiny,'\' + \'"/Rshiny/www/micophone/audio.wav"\').save_em_audio();',
           'em_text = speech2text.emotion.emo.EmotionText(\'',language,'\').save_em_text();',
           'speech2text.emotion.emo.final_emotion(em_text, em_audio)"')
  )
  return(print(vroom::vroom(paste0(path_shiny,"/Rshiny/output/output.txt"),delim = ".")))
}






