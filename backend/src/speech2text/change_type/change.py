from pydub import AudioSegment

def wav(input_file):
    if input_file.endswith('.mp3'):
        sound = AudioSegment.from_mp3(input_file)
        sound.export(input_file.replace(".mp3", ".wav"), format="wav")
        input_file = input_file.replace(".mp3", ".wav")
    elif input_file.endswith('.wav'):
        input_file = input_file
    return input_file