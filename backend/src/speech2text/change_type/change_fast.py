from pydub import AudioSegment

def wav_fast(input_file):
    if input_file.endswith('.mp3'):
        sound = AudioSegment.from_mp3(input_file)
        input_file = sound.export(input_file.replace(".mp3", ".wav"), format="wav")

    elif input_file.endswith('.wav'):
        input_file = input_file
    return input_file

# wav_fast("C:/Users/KaichengLi/PycharmProjects/my_project/audio/en_1.mp3")
# wav("C:/Users/KaichengLi/PycharmProjects/my_project/Rshiny/www/micophone/audio.mp3")
################################################
# from pydub import AudioSegment
# import wave
# import logging
#
# input_file = "C:/Users/KaichengLi/PycharmProjects/my_project/Rshiny/www/micophone/audio.mp3"
# sound = AudioSegment.from_mp3(input_file)
# sound.export(input_file.replace(".mp3", ".wav"), format="wav", codec='libmp3lame')

#################################################
# # 读取mp3的波形数据
# # sound = AudioSegment.from_file("C:/Users/KaichengLi/PycharmProjects/my_project/Rshiny/www/micophone/audio.mp3", format='MP3')
# sound = AudioSegment.empty()
#
# l = logging.getLogger("pydub.converter")
# l.setLevel(logging.DEBUG)
# l.addHandler(logging.StreamHandler())
# input_file = "C:/Users/KaichengLi/PycharmProjects/my_project/Rshiny/www/micophone/audio.mp3"
#
# sound.export(input_file.replace(".mp3", ".wav"), format="wav", codec='libmp3lame')
# input_file = input_file.replace(".mp3", ".wav")

# # 将读取的波形数据转化为wav
# f = wave.open("777.wav", 'wb')
# f.setnchannels(1)   # 频道数
# f.setsampwidth(2)   # 量化位数
# f.setframerate(16000)   # 取样频率
# f.setnframes(len(sound._data))   # 取样点数，波形数据的长度
# f.writeframes(sound._data)   # 写入波形数据
# f.close()
