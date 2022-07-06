#import mysql.connector
from modules.convert_audio.convert import convert_mp3
from gtts import gTTS
import sqlite3
import datetime
import conf as cf
import random
import numpy as np



def connect_mysql(host=cf.BD_HOST, user=cf.BD_USER, password=cf.BD_PASSWORD, database=cf.BD_NAME):
    conn = mysql.connector.connect(
        host=host, user=user, password=password, database=database)
    return conn


def connect_sqlite(database=cf.PATH_BD):
    conn = sqlite3.connect(database)
    return conn

     
def handle_decision(agi , message , file_path , values = ['1' , '2']):
    user_rep = ''
    while user_rep not in values:
        user_rep = read_message(message, file_path , agi)
        
    return user_rep


def interact(agi, nodes):
    length = len(nodes)
    values = []
    
    for i in range(1,length+1):
        values.append(str(i))
        
    
    formulation = formulate(nodes)
    user_rep = read_message(formulation, cf.REAL_PATH_AUDIO.format(
        nom="/formulation", thread_id=agi.env["agi_threadid"]), agi)
    
    # on repete ca tant que l'utilisateur n'entre rien ou un mauvais choix
    while user_rep not in values:
        user_rep = read_message(formulation, cf.REAL_PATH_AUDIO.format(
            nom="/formulation", thread_id=agi.env["agi_threadid"]), agi)
        
    return nodes[int(user_rep)-1][0] , int(user_rep)


def handle_IVR(agi):
    conn = connect_sqlite()
    racines = load_nodes(conn, agi, racine=True)
    length = len(racines)
    if length >= 1:
       repeat = True
       message = "voulez vous retourner au menu principale ? tapez 1 pour retourner . Tapez 2 pour quitter"
       #agi.verbose("---------------------------- condition ------")
       while repeat == True:
           id , user_rep = interact(agi , racines)
           handle_IVR_bis(agi, conn, id,
                          racines[user_rep - 1][1], racines[user_rep - 1][2])
           user_rep = handle_decision(agi, message, cf.REAL_PATH_AUDIO.format(
               nom="/formulation", thread_id=agi.env["agi_threadid"]))
           #agi.verbose("---------------------------- continue ------")
           if int(user_rep) == 1:
               repeat = True
           else:
               repeat = False
    
    
    
def handle_IVR_bis(agi , conn , node_id , nom ,  question):
    message = ""
    if question == None or question == '':
        message = cf.DEFAULT_MESSAGE + nom
    else:
        message = question
        
    read_message(message, cf.REAL_PATH_AUDIO.format(
        nom="/formulation", thread_id=agi.env["agi_threadid"]), agi, interrupt=False)
    nodes = load_nodes(conn, agi , id = node_id)
    
    length = len(nodes)
    if(length == 0):
        message = "arriver sur une feuille"
        user_rep = read_message(message, cf.REAL_PATH_AUDIO.format(
            nom="/formulation", thread_id=agi.env["agi_threadid"]), agi)
        sheet_id = load_sheet(conn , agi , node_id)
        if sheet_id == None:
            message = "aucune information sur cette feuille"
        else:
            information = load_information(conn, agi, sheet_id)
            #agi.verbose(f"**          {information}           ******")
            if information == None:
                message = "l'information sur cette feuille n'est plus valide"
            else:
                message = information
                
            #agi.verbose(f"**          {information}           ******")
            read_message(message, cf.REAL_PATH_AUDIO.format(
                nom="/formulation", thread_id=agi.env["agi_threadid"]), agi, interrupt=False)
    else:
        id , user_rep = interact(agi , nodes)
        #agi.verbose(f"---------------------------- id : {id}  choix : {user_rep} nom : {nodes[user_rep - 1][1]} question : {nodes[user_rep - 1][2]}!!!!!!!!!!!!!!!!!!!!!!!!!!!!!------")
        handle_IVR_bis(agi, conn, id ,
                       nodes[user_rep - 1][1], nodes[user_rep - 1][2])


def read_message(message, file_path, agi, interrupt = True):
    tts = gTTS(message, lang='fr')
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
        node = (row[0], row[1] , row[2])
        # agi.verbose(
        #     f"**     {row[0]} : {row[1]} , {row[2]} , {row[3]}         **")
        
        result.append(node)

    return result


def load_sheet(mysql_conn, agi, id):
    cursor = mysql_conn.cursor()
    
    cursor.execute(
        """SELECT administration_noeud.id 
                FROM administration_feuille INNER JOIN administration_noeud  
                ON administration_noeud.id = administration_feuille.noeud_ptr_id
                WHERE administration_noeud.id = {}""".format(id))
    
    rows = cursor.fetchall()
    if len(rows) == 0:
        return None
    else:
        return id

def load_information(mysql_conn, agi, id):
    result = []
    cursor = mysql_conn.cursor()
    # agi.verbose(f"**preparation de la requete pour avoir les valeurs de caracteristique **")
    cursor.execute(
        #id pos 0                                      nom pos 1                            content pos 2                          type pos 3
        """SELECT administration_caracteristique.id , administration_caracteristique.nom , enseignant_valcaracteristique.content , administration_caracteristique.type
                FROM administration_caracteristique , enseignant_valcaracteristique , enseignant_information 
                WHERE
                administration_caracteristique.id = enseignant_valcaracteristique.caracteristique_id AND
                administration_caracteristique.feuille_id = {} AND 
                enseignant_information.delai > {}
                """.format(id, datetime.date.today()))

    val_caracteristiques = cursor.fetchall()
    # agi.verbose(f"**        pass premiere requete   ******")
    
    cursor.execute("""
            SELECT format_formulation ,  caracteristiques
            FROM administration_formulation 
            WHERE
                feuille_id = {}
            """.format(id))
    
    # agi.verbose(f"**        pass deux requetes   ******")
    formats_list = cursor.fetchall()
    #dans le cas ou il n'y a aucune valeur de carcaterisques
    if len(val_caracteristiques) == 0:
        return None
    #dans le cas ou il n'y aucun format de formulation associe a la feuille en question
    elif len(formats_list) == 0:
        information = ""
        for val_c in val_caracteristiques:
            information += val_c[1] + " : " + val_c[2]

        return information
    else:
        format = random.choice(formats_list)

        ids_list = format[1].split(";")
        template = format[0]
        order_val_caracteristique = []

        for id in ids_list:
            order_val_caracteristique += [
                val_c for val_c in val_caracteristiques if int(id) in val_c]

        for val_c in order_val_caracteristique:
            if val_c[3] != "date":
                template = template.replace("[value]", val_c[2], 1)
            else:
                #on recherche les idex des premieres occurences de tous les formats de date
                begin_index = [template.find(cf.DATE_FORMAT[i])
                            for i in range(len(cf.DATE_FORMAT))]

                begin_index = np.array(begin_index)
                begin_index = np.where(begin_index >= 0, begin_index, len(template))

                pos = np.argmin(begin_index)
                if cf.DATE_FORMAT[pos] == "[value]":
                    template = template.replace("[value]", val_c[2], 1)
                else:
                    temp = cf.DATE_FORMAT[pos].lower()
                    date_part = val_c[2].split(" ")
                    first_part = date_part[0].split("-")
                    second_part = date_part[1].split(":")
                    replace_value = ""
                    if "yy".lower() in temp:
                        replace_value = first_part[0]
                    elif "mm".lower() in temp:
                        replace_value = first_part[1]
                    elif "dd".lower() in temp:
                        replace_value = first_part[2]
                    elif "hh".lower() in temp:
                        replace_value = second_part[0]
                    elif "mm".lower() in temp:
                        replace_value = second_part[1]
                    else:
                        replace_value = second_part[2]

                    template = template.replace(temp, replace_value)

        return template



def formulate(nodes):
    i = 1
    result = ""
    for node in nodes:
        result += f"Tapez {str(i)} pour {node[1]}. "
        i = i + 1

    return result



