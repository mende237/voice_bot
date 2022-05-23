#!/home/dimitri/anaconda3/bin/python3

# import imp
import conf as cf
#from modules.asterisk.agi import Agi
from asterisk.agi import *
from handle_IVR import handle_IVR

agi = AGI()
agi.verbose(""" enter menu !!!!!!!!!!!!!!!!!!!!!!""")
r = handle_IVR(agi)
#agi.stream_file(cf.CHEMIN_AUDIOS_APP+"/welcome")
agi.verbose(""" passs ???????????????????????????""")

exit(0)
