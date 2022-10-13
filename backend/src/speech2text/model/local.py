import os
import warnings
import librosa
from .. import config
from .. import cut_audio
from .. import change_type

output_path = config.Rshiny_path + "/Rshiny"

warnings.filterwarnings('ignore')

# speech to text
def rec_doc(input_audio, language, output_ad=output_path):
    # # change mp3 to wav in fast way
    wav_audio = change_type.fast.wav(input_audio)

    from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer
    '''
    Effectuer la reconnaissance vocale sur tous les fichiers coupés du dossier, aussi enregistre
    '''
    # output file
    output_address = os.path.join(output_ad, "output")

    # language
    if language == "EN":
        tokenizer = Wav2Vec2Tokenizer.from_pretrained(config.model_path + "/model/s2t-en")
        model = Wav2Vec2ForCTC.from_pretrained(config.model_path + "/model/s2t-en")
    elif language == "FR":
        tokenizer = Wav2Vec2Tokenizer.from_pretrained(config.model_path + "/model/s2t-fr2")
        model = Wav2Vec2ForCTC.from_pretrained(config.model_path + "/model/s2t-fr2")
    print(wav_audio)

    # don't need to cut_audio if<= 1 min
    if librosa.get_duration(filename=wav_audio) <= 60:
        # recognition
        audio_text = _predict(wav_audio, tokenizer=tokenizer, model=model)
        # chunk_audio_text_punctuation = punctuation(chunk_audio_text)
        # chunk_audio_text_final = chunk_audio_text.capitalize()
        text = audio_text.lower()
    else:
        cut_audio.cut.CUT(wav_audio, output_address)
        # recognition
        text = ''
        for root, dirs, files in os.walk(output_address + "/chunks"):
            for file in files:
                if file.split('.')[-1] == 'wav':
                    sub_adress = output_address + "/chunks/" + file
                    chunk_audio_text = _predict(sub_adress, tokenizer=tokenizer, model=model)
                    print("did one part")
                    # chunk_audio_text_punctuation = punctuation(chunk_audio_text)
                    # chunk_audio_text_final = chunk_audio_text.capitalize()
                    text = '{}{}'.format(text, chunk_audio_text)
                text = text.lower()
    print(output_address)
    # Save output in file
    with open(os.path.join(output_address + "/output_history.txt"), 'a+', encoding="utf-8") as file:
        file.writelines([text + "\n"])

    with open(os.path.join(output_address + "/output.txt"), 'w', encoding="utf-8") as file:
        file.writelines([text + "\n"])
    print(text)
    return text


def _predict(input_file, tokenizer, model):
    import torch ,librosa
    speech, rate = librosa.load(input_file, sr=16000)
    # pt mean pytroch
    input_values = tokenizer(speech, return_tensors='pt').input_values
    # Store logits(non-normalized predictions)
    logits_audio = model(input_values)
    logits = logits_audio.logits
    # store predicted id's
    predicted_ids = torch.argmax(logits, dim=-1)

    transcriptions = tokenizer.decode(predicted_ids[0])
    return transcriptions



