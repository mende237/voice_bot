import mysql.connector
from modules.convert_audio.convert import convert_mp3
from gtts import gTTS
import conf as cf


def connect(host=cf.BD_HOST, user=cf.BD_USER, password=cf.BD_PASSWORD, database=cf.BD_NAME):
    conn = mysql.connector.connect(
        host=host, user=user, password=password, database=database)
    return conn


def greet(agi, welcome_message="bienvenu dans notre programme d'accès à l'information"):
    read_message(welcome_message, cf.CHEMIN_AUDIOS_APP +
                 "/welcome.mp3", agi , interrupt = False)
    
def handle_decision(agi , message):
    values = ['1' , '2']
    while user_rep not in values:
        user_rep = read_message(message , cf.CHEMIN_AUDIOS_APP +
                            "/formulation.mp3", agi)
    return user_rep


def interact(agi, nodes):
    length = len(nodes)
    values = []
    
    for i in range(1,length+1):
        values.append(str(i))
        
    
    formulation = formulate(nodes)
    user_rep = read_message(formulation, cf.CHEMIN_AUDIOS_APP +
                            "/formulation.mp3", agi)
    
    agi.verbose(
        f"le reponse ---------------------- {values} ------")
    # on repete ca tant que l'utilisateur n'entre rien ou un mauvais choix
    while user_rep not in values:
        user_rep = read_message(formulation, cf.CHEMIN_AUDIOS_APP +
                                "/formulation.mp3", agi)
       
    return user_rep


def handle_IVR(agi):
    conn = connect()
    racines = load_nodes(conn, agi, racine=True)
    length = len(racines)
    greet(agi)
    if length >= 1:
       repeat = True
       message = "voulez vous retourner au menu principale ? tapez 1 pour retourner . Tapez 2 pour quitter"
       agi.verbose("---------------------------- condition ------")
       while repeat == True:
           user_rep = interact(agi , racines)
           agi.verbose("---------------------------- continue ------")
           handle_IVR_bis(agi , conn , int(user_rep))
           user_rep = handle_decision(message)
           if int(user_rep) == 1:
               repeat = True
           else:
               repeat = False
    
    
def handle_IVR_bis(agi , conn , node_id):
    nodes = load_nodes(conn, agi , id = node_id)
    length = len(nodes)
    if(length == 0):
        message = "arriver sur une feuille"
        user_rep = read_message(message, cf.CHEMIN_AUDIOS_APP +
                            "/formulation.mp3", agi)
    else:
        user_rep = interact(agi , nodes)
        handle_IVR_bis(agi , conn , int(user_rep))


def read_message(message, file_path, agi, interrupt = True):
    tts = gTTS(message, lang='fr')
    agi.verbose(f"***     {file_path}        ***")
    tts.save(file_path)

    new_file = file_path.replace('.mp3', '.wav')
    convert_mp3(file_path, new_file)
    if interrupt == True:
        rep = agi.get_data(new_file.replace('.wav', ''))
    else:
        rep = agi.stream_file(new_file.replace('.wav', ''))
    return rep


# racine est un booleen mettre a false si l'on veut charger des noeud intermediaires
def load_nodes(mysql_conn, agi, id=-1, racine=False):
    result = []
    cursor = mysql_conn.cursor()
    if racine == False:
        cursor.execute(
            """SELECT * FROM administration_noeud WHERE parent_id = {}""".format(id))
    else:
        cursor.execute(
            """SELECT * FROM administration_noeud WHERE parent_id IS NULL""")

    rows = cursor.fetchall()
    for row in rows:
        node = (row[0], row[1] , row[3])
        agi.verbose(
            f"**     {row[0]} : {row[1]} , {row[2]} , {row[3]}         **")
        result.append(node)

    return result


def formulate(nodes):
    i = 1
    result = ""
    for node in nodes:
        result += f"Tapez {str(i)} pour {node[1]}. "
        i = i + 1

    return result



