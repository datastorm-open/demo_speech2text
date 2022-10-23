from pydub import AudioSegment

def wav(input_file):
    if input_file.endswith('.mp3'):
        sound = AudioSegment.from_mp3(input_file)
        out_file = input_file.replace(".mp3", ".wav")
        sound.export(out_file, format="wav")
        # out_file = "/".join(re.split(r' |/|\\|[\s,.]', input_file)[0:-1]) + ".wav"
        return out_file
    elif input_file.endswith('.wav'):
        out_file = input_file
        return out_file
