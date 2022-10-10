from .. import config
from .. import api
from .. import change_type

output_path = config.Rshiny_path + "/Rshiny"
mico_path = config.Rshiny_path + "/Rshiny/www/micophone/audio.mp3"


def mico_API(language, input_audio=mico_path, output_adress=output_path):
    change_type.mico.wav(input_audio)
    input_audio_wav = config.Rshiny_path + "/Rshiny/www/micophone/audio.wav"
    api.api_doc.API_document(input_audio_wav, language, output_adress)
