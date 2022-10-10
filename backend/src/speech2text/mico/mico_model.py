import os

from .. import config
from .. import model

def mico_Loc(input_audio = config.mico_path, output_adress= config.output_path, language="EN"):
    model.local.rec_doc(input_audio, output_adress, language)
