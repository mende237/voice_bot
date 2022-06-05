import speech_recognition as sr
from handle_IVR import handle_decision, read_message
import conf as cf


def create_sample_from_test_file(file_name):
    wavfile = sr.WavFile(file_name)
    with wavfile as source:
        return sr.AudioData(
            source.stream.read(), wavfile.SAMPLE_RATE,
            wavfile.SAMPLE_WIDTH)

def handle_direct_question(agi):
    user_rep = ""
    file_path = cf.REAL_PATH_AUDIO.format(nom="/question", thread_id=agi.env["agi_threadid"])
    file_path = file_path.replace(".mp3" , "")
    agi.verbose(f"**          {file_path}           ******")
    while user_rep != "1":
        message = "tapez 1: pour commencer l'enregistrement de votre question, et pour envoyer tapez 2 ."
        read_message(message, cf.REAL_PATH_AUDIO.format(
            nom="/formulation", thread_id=agi.env["agi_threadid"]), agi, interrupt=False)


        message = "êtes vous prêt pour commencer l'enregistrement ? tapez 1 pour oui,tapez 2 pour non"
        user_rep = handle_decision(agi, message, cf.REAL_PATH_AUDIO.format(
            nom="/formulation", thread_id=agi.env["agi_threadid"]))
        
        if user_rep == "1":
            break
        
    r = sr.Recognizer()
    rep_asterisk = agi.record_file(file_path , format = "wav", escape_digits = "2", timeout=60000)
    audio_data = create_sample_from_test_file(file_path+'.wav')
    agi.verbose(f"********            pass creation audio data        **********")
    try:
        text = r.recognize_google(audio_data, language="fr-FR")
        agi.verbose(f"********            pass asr         **********")
        agi.verbose(f"**          {text}           ******")
    except Exception as e:
        agi.verbose(f"**         {e}          ******")
    
    
    # if rep_asterisk == '-1':
    #     # une erreur c'est produite
    #     agi.verbose(f"**          une erreur c'est produite           ******")
    #     pass

    # message = "fin de l'enregistrement"
    # read_message(message, cf.REAL_PATH_AUDIO.format(
    #     nom="/formulation", thread_id=agi.env["agi_threadid"]), agi, interrupt=False)
    pass



