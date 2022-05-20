import mysql.connector
from modules.convert_audio.convert import convert_mp3
from gtts import gTTS
import conf as cf


def connect(host=cf.BD_HOST, user=cf.BD_USER, password=cf.BD_PASSWORD, database=cf.BD_NAME):
    conn = mysql.connector.connect(
        host=host, user=user, password=password, database=database)
    return conn


def handle_IVR(agi):
    agi.verbose("""******************* enter IVR *************""")
    conn = connect()
    repeat = True
    welcome_message = "bienvenu dans notre programme d'accès à l'information"
    read_message(welcome_message, cf.CHEMIN_AUDIOS_APP +
                 "/welcome.mp3" , [] , agi)

    level_racine = True
    while repeat == True:
        if level_racine:
            racines = load_nodes(conn, agi, racine=True)
            length = len(racines)
            values = [range(1, length+1)]
            formulation = formulate(racines)
            agi.verbose(f"******************* {formulation} *************")
            agi.verbose("***            racine             ***")
            user_rep = read_message(formulation, cf.CHEMIN_AUDIOS_APP +
                               "/formulation.mp3", values , agi)

            agi.verbose(
                f"le nombre de racine est  ---------------------- {length} ------")
            agi.verbose(f"le reponse ---------------------- {user_rep} ------")

            # on repete ca tant que l'utilisateur n'entre rien ou un mauvais choix
            while user_rep not in values:
                user_rep = read_message(formulation, cf.CHEMIN_AUDIOS_APP +
                                   "/formulation.mp3", values , agi)
                agi.verbose(
                    f"le reponse ---------------------- {user_rep} ------")
                
        else:
            agi.verbose("***            noeud!!!!!!!        ***")
            # nodes = load_nodes(conn , agi , id = id)
        repeat = False
    return 0


def read_message(message, file_path, escape_digits , agi):
    tts = gTTS(message, lang='fr')
    agi.verbose(f"***     {file_path}        ***")
    tts.save(file_path)

    new_file = file_path.replace('.mp3', '.wav')
    convert_mp3(file_path, new_file)
    if len(escape_digits) == 0:
        agi.stream_file(new_file.replace('.wav', ''))
    else:
        agi.stream_file(new_file.replace('.wav', ''),
                        escape_digits=escape_digits)
    return 0


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
        node = (row[0], row[1])
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


