import sys

class Agi(object):

    def __init__(self):
        # on recupere les variables d'environnement envoye par asterisk
        self.asterisk_env = {}

    def loading(self):
        while True:
            line = sys.stdin.readline().strip()
            if not len(line):
                break
            var_name, var_value = line.split(':', 1)
            self.asterisk_env[var_name] = var_value

    def agi_command(self, cmd):
        '''permet d'envoyer une requette au serveur asterisk et d'obtenir un resultat a la requete'''

        # on ecrit la requete sur la sortie standard qui sera execute
        print(str(cmd))

        # on vide la sortie standard
        sys.stdout.flush()

        # on recupere le resultat sur la sortie standard avec suppression des espace blancs
        return sys.stdin.readline().strip()

    def playback(self, path_sound):
        self.agi_command('STREAM FILE '+str(path_sound)+' "" ')

    def get_data(self, path_sound, timeout=1000, max_digits=8):
        param = str(path_sound)
        if timeout is not None:
            param += " "+str(timeout)
            if max_digits is not None:
                param += " "+str(max_digits)
        response = self.agi_command("GET DATA "+param)
        if 'timeout' in response:
            return "-1"
        return response.split('=', 1)[1]

    def record(self, path_filename, format, max_time_record, max_time_silence):
        return self.agi_command('RECORD FILE '+str(path_filename)+' '+str(format)+' "" '+str(max_time_record)+' s='+str(max_time_silence))

    def answer(self):
        return self.agi_command('ANSWER')

    def hangup(self):
        return self.agi_command('HANGUP')
