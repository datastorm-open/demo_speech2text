import torch
import torch.nn.functional as F
import torchaudio
from transformers import AutoConfig, Wav2Vec2FeatureExtractor
from .emo_dep.models import Wav2Vec2ForSpeechClassification
from transformers import pipeline
import pandas as pd
from .. import config

model_path = config.model_path
save_path = config.Rshiny_path
text_path = save_path
# model_path = "C:/Users/scofi/PycharmProjects/app"
# save_path = "C:/Users/scofi/PycharmProjects/app"

# for tone
class EmotionAudio:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model_name_or_path = model_path + "/model/emotion_audio"
    config = AutoConfig.from_pretrained(model_name_or_path)
    feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(model_name_or_path)
    sampling_rate = feature_extractor.sampling_rate
    model = Wav2Vec2ForSpeechClassification.from_pretrained(model_name_or_path).to(device)

    def __init__(self,path):
        self.path = path

    def _speech_file_to_array_fn(path):
        speech_array, sampling_rate = torchaudio.load(path)
        resampler = torchaudio.transforms.Resample(sampling_rate)
        speech = resampler(speech_array).squeeze().numpy()
        return speech

    def _predict(path,sampling_rate):
        speech = EmotionAudio._speech_file_to_array_fn(path)
        inputs = EmotionAudio.feature_extractor(speech, sampling_rate=sampling_rate, return_tensors="pt", padding=True)
        inputs = {key: inputs[key].to(EmotionAudio.device) for key in inputs}
        with torch.no_grad():
            logits = EmotionAudio.model(**inputs).logits
        scores = F.softmax(logits, dim=1).detach().cpu().numpy()[0]
        outputs = [{"Emotion": EmotionAudio.config.id2label[i], "Score": f"{round(score * 100, 3):.1f}%"} for i, score in
                   enumerate(scores)]
        return outputs

    def save_em_audio(self):
        em_audio = EmotionAudio._predict(self.path, EmotionAudio.sampling_rate)
        print(em_audio)
        em_audio_fianl = pd.DataFrame(columns=['Emotion', 'Score'], data=em_audio)
        for i in range(0, len(em_audio_fianl['Score'])):
            em_audio_fianl['Score'][i] = float(em_audio_fianl['Score'][i].strip('%')) / 100
        em_audio_fianl.to_csv(save_path + '/Rshiny/output/emotion/em_tone.csv', encoding='utf-8', sep=",")
        print("************em_audio*************")
        print(em_audio_fianl)
        print('*************************')
        return em_audio_fianl

#####################################################################################

class EmotionText:
    def __init__(self, language):
        self.language = language

    # need absolute path
    def save_em_text(self):
        classifier = pipeline("text-classification",
                              model=model_path + '/model/emotion_text',
                              return_all_scores=True)

        f = open(text_path + "/Rshiny/output/output.txt", encoding="utf-8")
        print(f.read())

        if self.language == "EN":
            # API_document(path, language)
            em_text = classifier(text_path + "/Rshiny/output/output.txt")

        elif self.language == "FR":
            from translate import Translator

            with open(text_path + "/Rshiny/output/output.txt") as file:
                text = file.read()
            translator = Translator(from_lang='fr', to_lang="English")
            translation = translator.translate(text)

            print(translation)
            em_text = classifier(translation)

        else:
            raise Exception("wrong input")

        em_text = pd.DataFrame(em_text[0])
        columns_map = {
            'label': 'Emotion',
            'score': 'Score'
        }
        em_text.rename(columns=columns_map, inplace=True)
        em_text.iloc[1, 0] = "happiness"
        em_text.to_csv(save_path + '/Rshiny/output/emotion/em_text.csv', encoding='utf-8', sep=",")
        print("************em_text*************")
        print(em_text)
        print("*******************************************")
        return em_text

#########################################################################################
def final_emotion(em_text,em_audio):

    new = pd.DataFrame(columns=['Emotion','Score'], index=[list(range(0, 7))])
    new.Emotion = ['anger', 'fear', 'happiness', 'love', 'sadness', 'surprise', 'disgust']
    final = pd.DataFrame(columns=['Emotion','Score'], index=[list(range(0, 7))])
    final.Emotion = ['anger', 'fear', 'happiness', 'love', 'sadness', 'surprise', 'disgust']

    print("*************em_final***************")
    new.Score[new.Emotion =='anger'    ] = float(em_text[(em_text.Emotion == 'anger')]['Score'])+float(em_audio.loc[(em_audio.Emotion=='anger')]['Score'])
    new.Score[new.Emotion =='fear'     ] = float(em_text[(em_text.Emotion == 'fear')]['Score'])+float(em_audio.loc[(em_audio.Emotion=='fear')]['Score'])
    new.Score[new.Emotion =='happiness'] = float(em_text[(em_text.Emotion == 'happiness')]['Score'])+float(em_audio.loc[(em_audio.Emotion=='happiness')]['Score'])
    new.Score[new.Emotion =='love'     ] = float(em_text[(em_text.Emotion == 'love')]['Score'])*2
    new.Score[new.Emotion =='sadness'  ] = float(em_text[(em_text.Emotion == 'sadness')]['Score'])+float(em_audio.loc[(em_audio.Emotion=='sadness')]['Score'])
    new.Score[new.Emotion =='surprise' ] = float(em_text[(em_text.Emotion == 'surprise')]['Score'])*2
    new.Score[new.Emotion =='disgust'  ] = float(em_audio.loc[(em_audio.Emotion == 'disgust')]['Score'])*2

    print(new)
    print(sum(new.Score))
    print("*************Normalisation***************")
    final.Score[final.Emotion =='anger']     = new.Score[new.Emotion =='anger']/sum(new.Score)
    final.Score[final.Emotion =='fear']      = new.Score[new.Emotion =='fear']/sum(new.Score)
    final.Score[final.Emotion =='happiness'] = new.Score[new.Emotion =='happiness']/sum(new.Score)
    final.Score[final.Emotion =='love']      = new.Score[new.Emotion =='love']/sum(new.Score)
    final.Score[final.Emotion =='sadness']   = new.Score[new.Emotion =='sadness']/sum(new.Score)
    final.Score[final.Emotion =='surprise']  = new.Score[new.Emotion =='surprise']/sum(new.Score)
    final.Score[final.Emotion =='disgust']   = new.Score[new.Emotion =='disgust'] /sum(new.Score)
    print(sum(final.Score))
    print(final)

    final.to_csv(save_path+'/emotion/em_final.csv', encoding='utf-8', sep=",")
    return final
