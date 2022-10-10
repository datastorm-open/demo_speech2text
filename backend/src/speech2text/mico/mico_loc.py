from .. import config
from .. import model
from .. import change_type

output_path = config.Rshiny_path + "/Rshiny"
mico_path = config.Rshiny_path + "/Rshiny/www/micophone/audio.mp3"


def mico_LOC(language, input_audio=mico_path, output_adress=output_path):
    change_type.mico.wav(input_audio)
    input_audio_wav = config.Rshiny_path + "/Rshiny/www/micophone/audio.wav"
    model.local.rec_doc(input_audio_wav, language, output_adress)
