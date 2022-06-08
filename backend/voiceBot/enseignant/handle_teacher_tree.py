import datetime
from audioop import reverse

from administration.models import Caracteristique, Feuille, Noeud
from django.urls import reverse

from enseignant.models import Information, ValCaracteristique


def node_tohtml(node):
    children = node.noeud_set.all()
    n = len(children)
    nom = "<h5 class=\"m-0 mx-3\">" + node.nom + "</h5>"

    #id {id} peut etre l'id de l'information dans le cas d'une modification ou id d'une feuille de cas de l'ajout
    form_delete = """<div class = "d-flex p-1">
                        <form action=" """ + reverse('enseignantin:view_form') + """" method="get" class = "w-100"> 
                           <input type="hidden" name="id" value="{id}">
                           <input type="hidden" name="add_or_modif" value="{add_or_modif}">
                           <button type="submit" class="w-100 btn btn-primary">{message}</button>
                        </form>  
                        </div>"""
    
    if(n == 0):
        # on verifie si la feuille a deja ete defini comme feuille
        if len(Feuille.objects.filter(id=node.id)) != 0:
            infos = Information.objects.filter(valcaracteristique__caracteristique__feuille__id=node.id)
            modifier = ""
            if len(infos) != 0:
                info = infos[0]
                # for i in range(len(infos)):
                #     temp_info = infos[i]
                #     if temp_info.delai > max_info.delai:
                #         max_info = temp_info
            
                form_delete = form_delete.format(id=info.id, message="modifier", add_or_modif = "modifier")
            else:
                form_delete = form_delete.format(id=node.id, message="ajouter", add_or_modif="ajouter")
            # if len(infos) != 0:
            #     info = infos[0]
            #     modifier = """<form action=" """ + reverse('enseignantin:view_form_with_default_value') + """" method="get" class = "w-100 mr-1"> 
            #                     <input type="hidden" name="id" value=" """ + str(info.id) + """ ">
            #                     <button type="submit" class="w-100 btn btn-primary">modifier</button>
            #                     </form>"""
                
            form_delete = form_delete.format(modif = modifier)
            return """ <div class="d-flex align-items-center justify-content-between">
                             <div class="btn d-inline-flex align-items-center gap-2">
                                 <i class="fa fa-file"></i> """ + nom + """
                             </div>
                             <div class="btn-group">
                            """+form_delete+"""
                        </div>
                    </div> """
        # construction de la vue d'une noeud terminal
        return """ <div class="d-flex align-items-center justify-content-between">
                             <div class="btn d-inline-flex align-items-center ">
                                 <i class="fa fa-folder"></i> """ + nom + """
                             </div>
                         </div> """
                

    # contruction du html noeud
    icon = """<i class="fa fa-folder"></i> """ if node.parent != None else """<i class="fa fa-sitemap"></i> """
    result = """
            <ul class="list-unstyled m-0 py-1">
             <div class="d-flex align-items-center justify-content-between">
                <button class="btn d-inline-flex align-items-center collapsed rounded-0 gap-2" data-bs-toggle="collapse" data-bs-target="#_"""+str(node.id)+"""" aria-expanded="false">
                    """ + icon + nom + """
                </button>
               
             </div> """

    # > insertion des enfants
    result += """ <div class="collapse list_node" id="_"""+str(node.id)+"""">
                    <ul class="list-unstyled">"""

    for child in children:
        res = node_tohtml(child)
        result += "<li>" + res + "</li>"
    result += "</ul></div></ul>"

    return result



def generate_hierachie():
    trees_visual = ""
    racines = Noeud.objects.filter(parent=None)
    modals = ""
    if(len(racines) != 0):
        for racine in racines:
            res = node_tohtml(racine)
            trees_visual += res
    else:
        trees_visual = trees_visual + "<h2> Aucun noeud existant </h2>"
    return trees_visual
