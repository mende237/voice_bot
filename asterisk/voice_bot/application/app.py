#!/usr/bin/env python3

import conf as cf
from modules.asterisk.agi import Agi


agi = Agi()
agi.loading()

reponse = agi.playback(cf.CHEMIN_AUDIOS_APP+"/test")

agi.hangup()
exit(0)
