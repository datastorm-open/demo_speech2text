
# Define UI for application that draws a histogram
shinyUI(fluidPage(
  
  # Application title
  titlePanel("Speech2Text"),
  
  # Sidebar with a slider input for the number of bins
  sidebarLayout(
    
    sidebarPanel(
      
      selectInput("select", label = h2("Choose The Language"), 
                  choices = c("Français" , "Anglais"), selected = "Français"),
      
      radioButtons("checkGroup", 
                         label = h3("Choose a method for speech recognition"), 
                         choices = list("API_Google", "Speechbrain"),
                         selected = "API_Google"),
      #h1("________________________"),
      h2("_____________________________"),
      #h3("____________________________________"),
      fileInput("file", label = h3("File Recognition:"), accept = c(".wav", ".mp3")),
      
      uiOutput("ui_play"),
      actionButton("stop", "Terminal Playback",icon = icon('stop')),
      br(),
      br(),
      #submitButton("Identité", icon("refresh")),
      actionButton("fileidentify", label = "File-Recognition",icon = icon('running')),
      br(),
      br(),
      h2("_____________________________"),
      h3("Microphone"),
      shinymicrophone::audioRecordButtons('main'),
      actionButton("microidentify", label = "Mico-Recognition",icon = icon('running')),
      br(),
      br(),
      h2("_____________________________"),
      h3("Add punctuation"),
      actionButton("punctuation",label = "Add-Punctuation",icon = icon('at')),
      
    ),
    
    # Show a plot of the generated distribution
    mainPanel(
      h1("Speech to Text"),
      br(),
      
      h3("File Information:"),
      tableOutput("table"),
      br(),
      
      h3("Output Text:"),
      tableOutput("inputfile"),
      br(),
      
      h3("Micophone Output Text:"),
      uiOutput("myAudio"),     #mico audio
      tableOutput("microtext"), #mico output text
      br(),
      
      h3("Output Text add punctuation:"),
      tableOutput("add_punctuation"),
      
      h3("Audio File emotion:"),
      plotOutput('Emotion_file'),
      
      h3("Microphone emotion:"),
      plotOutput('Emotion_micro')
    
    )
  )
))

