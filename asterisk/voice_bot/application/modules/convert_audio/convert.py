from pydub import AudioSegment


def convert_mp3(self, path_src, path_dest,frame_rate=8000, format_dest="wav"):
    sound = AudioSegment.from_mp3(path_src)
    sound.set_channels(1)
    sound = sound.set_frame_rate(frame_rate)
    sound.export(path_dest, format="wav")  
            
        
    