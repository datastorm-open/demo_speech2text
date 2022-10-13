import speech_recognition as sr
import os
import librosa
import sys
from .. import config
from .. import cut_audio
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

    # don't need to cut_audio if<= 1 min
    if librosa.get_duration(filename=wav_file) <= 120:
        # recognition

        with sr.AudioFile(wav_file) as source:
            # listen for the data (load cut_audio to memory)
            audio_data = r.record(source)
            # recognize (convert from speech to text)
        if language == "EN":
            audio_text = r.recognize_google(audio_data, language="en-US")
        elif language == "FR":
            audio_text = r.recognize_google(audio_data, language="fr-FR")
        else:
            raise Exception("please input language correctly")
        # chunk_audio_text_punctuation = punctuation(chunk_audio_text)
        # chunk_audio_text_final = chunk_audio_text.capitalize()
        text = audio_text.lower()
    else:
        cut_audio.cut.CUT(wav_file, output_adress, length_limit=120 * 1000)
        # recognition
        text = ''
        for root, dirs, files in os.walk(output_adress + "/chunks"):
            for file in files:
                if file.split('.')[-1] == 'wav':
                    sub_adress = output_adress + "/chunks/" + file
                    with sr.AudioFile(sub_adress) as source:
                        # listen for the data (load cut_audio to memory)
                        audio_data = r.record(source)
                        # recognize (convert from speech to text)
                    if language == "EN":
                        chunk_audio_text = r.recognize_google(audio_data, language="en-US")
                    elif language == "FR":
                        chunk_audio_text = r.recognize_google(audio_data, language="fr-FR")
                    else:
                        raise Exception("please input language correctly")
                    print("did one part")
                    # chunk_audio_text_punctuation = punctuation(chunk_audio_text)
                    # chunk_audio_text_final = chunk_audio_text.capitalize()
                    text = '{}{}'.format(text, chunk_audio_text)
                text = text.lower()
    print(output_adress)

    # Save output in file
    with open(os.path.join(output_adress + "/output_history.txt"), 'a+', encoding="utf-8") as file:
        file.writelines([text + "\n"])

    with open(os.path.join(output_adress + "/output.txt"), 'w', encoding="utf-8") as file:
        file.writelines([text + "\n"])
    return print(text)