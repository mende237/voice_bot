
# chemin de fichier de sauvegarde des fichiers de l'application
from unittest.mock import DEFAULT

PATH_MODEL = "/home/herman/Documents/Cours/Master1/Semestre2/Ueprojet/code/voice_bot/asterisk/voice_bot/application/modeles"
CHEMIN_FICHIER_APP = "/home/herman/Documents/Cours/Master1/Semestre2/Ueprojet/code/voice_bot/asterisk/voice_bot"
CHEMIN_AUDIOS_APP = "/home/herman/Documents/Cours/Master1/Semestre2/Ueprojet/code/voice_bot/asterisk/voice_bot/data/audios"
REAL_PATH_AUDIO = CHEMIN_AUDIOS_APP + "{nom}{thread_id}.mp3"

# parametres liees a la base de donnees
BD_USER = "root"
BD_PASSWORD = ""
BD_NAME = "voiceBot_db"
PATH_BD = "/home/herman/Documents/Cours/Master1/Semestre2/Ueprojet/code/voice_bot/backend/voiceBot/voiceBot.db.sqlite3"
BD_HOST = "localhost"
DEFAULT_MESSAGE = "avoir plus d'information sur le "
DATE_FORMAT = ["[value:ss]", "[value:mm]", "[value:hh]",
               "[value:dd]", "[value:mm]", "[value:yy]"]

