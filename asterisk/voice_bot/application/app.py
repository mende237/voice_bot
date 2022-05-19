#!/home/mbe/Bureau/DS/python/easylocalenv/bin/python3

import conf as cf
from modules.asterisk.agi import Agi
from modules.convert_audio.convert import convert_mp3
import mysql.connector

agi = Agi()
agi.loading()

reponse = agi.playback(cf.CHEMIN_AUDIOS_APP+"/test")

from gtts import gTTS
tts=gTTS("veuillez entrez un numero",lang='fr')
tts.save(cf.CHEMIN_AUDIOS_APP+"/ask_choise_1.mp3")

convert_mp3(cf.CHEMIN_AUDIOS_APP+"/ask_choise_1.mp3", cf.CHEMIN_AUDIOS_APP+"/ask_choise_1.wav")
reponse = agi.playback(cf.CHEMIN_AUDIOS_APP+"/ask_choise_1")

agi.hangup()
exit(0)
