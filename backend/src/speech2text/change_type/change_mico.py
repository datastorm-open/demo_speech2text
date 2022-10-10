import subprocess
import os
from .. import config
# from speech2text import config

output_path = config.Rshiny_path +"/Rshiny/www/micophone"
def wav_mico(input_file):
    if input_file.endswith('.mp3'):
        if os.path.exists(output_path + '/audio.wav') is True:
            os.remove(output_path + '/audio.wav')
        input_file = subprocess.call(['ffmpeg', '-i', input_file, output_path + '/audio.wav'])

    elif input_file.endswith('.wav'):
        input_file = input_file

    return input_file

# wav_mico("C:/Users/KaichengLi/PycharmProjects/my_project/Rshiny/www/micophone/audio.mp3")