#!/home/dimitri/anaconda3/bin/python3

import conf as cf
#from modules.asterisk.agi import Agi
from asterisk.agi import *
from handle_IVR import handle_IVR , read_message , handle_decision 
from handle_direct_question import handle_direct_question 



def greet(agi, welcome_message="bienvenu dans notre programme d'accès à l'information"):
    read_message(welcome_message, cf.REAL_PATH_AUDIO.format(
        nom="/welcome", thread_id=agi.env["agi_threadid"]), agi, interrupt=False)
    
def start(agi):
    greet(agi)
    message = "Si voulez vous acceder à l'information via un menu IVR tapez 1 . via une question direct tapez 2"
    user_rep = handle_decision(agi, message, cf.REAL_PATH_AUDIO.format(
        nom="/welcome", thread_id=agi.env["agi_threadid"]))

    if user_rep == "1":
        handle_IVR(agi)
    else:
        handle_direct_question(agi)


def end(agi):
    pass 

        
agi = AGI()

start(agi)
end(agi)

exit(0)
