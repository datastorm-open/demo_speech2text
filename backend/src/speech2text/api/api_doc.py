import speech_recognition as sr
import os
import sys
from .. import config
from .. import change_type

output_path = config.Rshiny_path + "/Rshiny"


def API_document(input_audio, language="EN", output_adress=output_path):
    # creat fold "output"
    output_adress = output_adress + "/output"
    if os.path.exists(output_adress) is False:
        os.mkdir(output_adress)

    # change mp3 to wav in fast way
    wav_file = change_type.fast.wav(input_audio)

    # initialize the recognizer
    r = sr.Recognizer()
    # open the file
    with sr.AudioFile(wav_file) as source:
        # listen for the data (load cut_audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
    if language == "EN":
        text = r.recognize_google(audio_data, language="en-US")
    elif language == "FR":
        text = r.recognize_google(audio_data, language="fr-FR")
    else:
        raise Exception("please input language correctly")

    # Save output in file
    with open(os.path.join(output_adress + "/output_history.txt"), 'a+', encoding="utf-8") as file:
        file.writelines([text + "\n"])

    with open(os.path.join(output_adress + "/output.txt"), 'w', encoding="utf-8") as file:
        file.writelines([text + "\n"])
    return print(text)


