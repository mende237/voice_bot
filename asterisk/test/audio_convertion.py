from os import path
from pydub import AudioSegment

# files                                                                         
src = "/home/mbe/Bureau/projectsdjango/voice_bot/asterisk/test/menu.mp3"
dst = "test.wav"

# convert wav to mp3                                                            
sound = AudioSegment.from_mp3(src)
sound.set_channels(1)
sound = sound.set_frame_rate(8000)
sound.export(dst, format="wav")