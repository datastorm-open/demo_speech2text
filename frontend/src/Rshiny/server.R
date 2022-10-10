shinyServer(function(input, output,session){
#################################
  output$table <- renderTable({input$file})
  
  observeEvent(input$file,{file.copy(input$file$datapath, "www",overwrite = TRUE)})
  
  # input file
  Identify <- eventReactive(input$fileidentify, {
     # have to use a function here
    
     req(input$file)
    
     file_path <- gsub("\\\\","/",input$file$datapath)
     ext <- tools::file_ext(input$file$name)
     switch(input$checkGroup,
            API_Google  = withProgress(message = "Traitement du fichier audio...", value = 0.5,  
                                        expr = {switch(input$select,
                                                       # validation the file
                                                       "Français" =  switch(ext,
                                                                            wav = doc_api(file_path,"FR"),
                                                                            mp3 = doc_api(file_path,"FR"),
                                                                            validate("Invalid file; Please upload a .wav, .mp3 file")
                                                       ),
                                                       "Anglais"  =  switch(ext,
                                                                            wav = doc_api(file_path,"EN"),
                                                                            mp3 = doc_api(file_path,"EN"),
                                                                            validate("Invalid file; Please upload a .wav, .mp3 file")
                                                       )
                    )
                  }),
            Speechbrain = withProgress(message = "Traitement du fichier audio...", value = 0.5,  
                                        expr = {switch(input$select,
                                                      # validation the file
                                                      "Français" =  switch(ext,
                                                                           wav = doc_loc(file_path,"FR"),
                                                                           mp3 = doc_loc(file_path,"FR"),
                                                                           validate("Invalid file; Please upload a .wav, .mp3 file")
                                                      ),
                                                      "Anglais"  =  switch(ext,
                                                                           wav = doc_loc(file_path,"EN"),
                                                                           mp3 = doc_loc(file_path,"EN"),
                                                                           validate("Invalid file; Please upload a .wav, .mp3 file")
                                                      )
                                       )
                                       }),
            # pas encore faire
            Huggingface = withProgress(message = "Traitement du fichier audio...", value = 0.5,  
                                        expr = {switch(input$select,
                                                      # validation the file
                                                      "Français" =  switch(ext,
                                                                           wav = s2t_api_fr(file_path),
                                                                           mp3 = s2t_api_fr(file_path),
                                                                           validate("Invalid file; Please upload a .wav, .mp3 file")
                                                      ),
                                                      "Anglais"  =  switch(ext,
                                                                           wav = s2t_api_en(file_path),
                                                                           mp3 = s2t_api_en(file_path),
                                                                           validate("Invalid file; Please upload a .wav, .mp3 file")
                                                      ),
                                                      "German"  =  switch(ext,
                                                                          wav = s2t_api_gm(file_path),
                                                                          mp3 = s2t_api_gm(file_path),
                                                                          validate("Invalid file; Please upload a .wav, .mp3 file")
                                                      )
                                       )
                                       })
            )
     
     
  })
  
  
  output$inputfile <- renderTable({Identify()})
  
  ############################
  # play audio
  
  output$ui_play <- renderUI({
    input$stop
    actionButton("play_audio", label = "Play Audio File",icon = icon('play-circle'))
  })
  
  observeEvent(input$play_audio, {
    req(input$file)
    ext <- tools::file_ext(input$file$name)
    
    #file.copy(input$file$datapath, "www",overwrite = TRUE)
    if (input$play_audio == 1){
      
      # file.copy(input$file$datapath, "www",overwrite = TRUE)
      
      switch(ext,
             wav = insertUI(selector = "#play_audio",
                            where = "afterEnd",
                            ui = tags$audio(src = "0.wav", type = "audio/wav",controls = NA,autoplay = T)),
             mp3 = insertUI(selector = "#play_audio",
                            where = "afterEnd",
                            ui = tags$audio(src = "0.mp3", type = "audio/mp3",controls = NA,autoplay = T)))
    }
  })
  
  
  ##############################

  ## micophone
  # save audio
  audio <- shinymicrophone::audioRecordServer('main')

  output$myAudio <- shinymicrophone::renderAudio(audio)

  observe({
    if(!is.null(audio())){
      # save
      shinymicrophone::writeMP3(audio(), 'www/micophone/audio.mp3')
      # save history
      fname = paste0('mico_', Sys.time(), '.mp3')
      fname = stringr::str_replace_all(fname, ' ', '_')
      fname = stringr::str_replace_all(fname, ':', '-')
      shinymicrophone::writeMP3(audio(), paste("www/micophone/" , fname, sep = ""))
    }
  })
  # mico-audio speech2text
  Miicophone <- eventReactive(input$micoidentify, {
    switch (input$checkGroup,
            API_Google  = withProgress(message = "Traitement du fichier audio...", value = 0.5,  
                                       expr = {switch(input$select,
                                                      # validation the file
                                                      "Français" = mico_api("FR"),
                                                       
                                                      "Anglais"  = mico_api("EN")
                                                      )
                                               }),
            Speechbrain = withProgress(message = "Traitement du fichier audio...", value = 0.5,  
                                       expr = {switch(input$select,
                                                      # validation the file
                                                      "Français" = mico_loc("FR"),
                                                      
                                                      "Anglais"  = mico_loc("EN")
                                       )
                                       }),
            # pas fini
            Huggingface = withProgress(message = "Traitement du fichier audio...", value = 0.5,  
                                       expr = {switch(input$select,
                                                      # validation the file
                                                      "Français" = mico_api("FR"),
                                                      
                                                      "Anglais"  = mico_api("EN")
                                       )
                                       }),
            )
    
    })

  output$micotext <- renderTable({
    Miicophone()
  })
############################
  
  #add punctuation
  Add_punctuation <- eventReactive(input$punctuation,{
    withProgress(message = "En cours d'ajout de ponctuation...", value = 0.5,  
                 expr = {
                   add_pun()
                 })
  })
  output$add_punctuation <- renderTable({Add_punctuation()})
  

  

})

