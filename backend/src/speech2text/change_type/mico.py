import subprocess
import os
from .. import config

output_path = config.Rshiny_path +"/Rshiny/www/micophone"
def wav(input_file):
    if input_file.endswith('.mp3'):
        if os.path.exists(output_path + '/audio.wav') is True:
            os.remove(output_path + '/audio.wav')
        out_file = subprocess.call(['ffmpeg', '-i', input_file, output_path + '/audio.wav'])
        return out_file

    elif input_file.endswith('.wav'):
        out_file = input_file
        return out_file


