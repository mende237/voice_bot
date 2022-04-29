from audioop import reverse
from administration.models import Caracteristique, Feuille, Noeud
from django.urls import reverse

def node_tohtml(node):
    children = node.noeud_set.all()
    n = len(children)
    nom = "<h5 class=\"m-0\">" + node.nom + "</h5>"

    form_delete = """   <form action=" """ + reverse('enseignantin:view_form') +"""" method="get" class = "w-100"> 
                           <input type="hidden" name="id" value=" """ + str(node.id) + """ ">
                           <button type="submit" class="w-100 btn btn-primary">ajouter</button>
                        </form>  """
    
    if(n == 0):
        # on verifie si la feuille a deja ete defini comme feuille
        if len(Feuille.objects.filter(id=node.id)) != 0:
            return """ <div class="d-flex align-items-center justify-content-between">
                             <div class="btn d-inline-flex align-items-center gap-2">
                                 <i class="fa fa-leaf"></i> """ + nom + """
                             </div>
                             <div class="btn-group">
                            """+form_delete+"""
                        </div>
                         </div> """
        # construction de la vue d'une noeud terminal
        return """ <div class="d-flex align-items-center justify-content-between">
                             <div class="btn d-inline-flex align-items-center ">
                                 <i class="fa fa-node"></i> """ + nom + """
                             </div>
                         </div> """
                

    # contruction du html noeud
    icon = """<i class="fa fa-chevron-right"></i> """ if node.parent != None else """<i class="fa fa-code-fork"></i> """
    result = """
            <ul class="list-unstyled m-0 py-1">
             <div class="d-flex align-items-center justify-content-between">
                <button class="btn d-inline-flex align-items-center collapsed rounded-0 gap-2" data-bs-toggle="collapse" data-bs-target="#_"""+str(node.id)+"""" aria-expanded="false">
                    """ + icon + nom + """
                </button>
               
             </div> """

    # > insertion des enfants
    result += """ <div class="collapse border-start ps-2" id="_"""+str(node.id)+"""">
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
