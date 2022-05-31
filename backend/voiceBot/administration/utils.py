from django.urls import reverse
from administration.models import Feuille, Noeud


def node_tohtml(node):
    children = node.noeud_set.all()
    n = len(children)
    nom = "<h5 class=\"m-0\">" + node.nom + "</h5>"

    form_delete = """   <form action=" """ + reverse('adminin:delete_noeud') + """ " method="get" class = "w-100"> 
                           <input type="hidden" name="id" value=" """ + str(node.id) + """ ">
                           <button type="submit" class="w-100 btn btn-primary">supprimer</button>
                        </form>  """
                        
    
    form_add = """  
                    <button type="button" class="btn btn-primary w-100" data-bs-toggle="modal" data-bs-target="#__"""+str(node.id)+"""">
                        ajouter
                    </button>
                    
                """
    modal_add = """
                    <div class="modal fade" id="__"""+str(node.id)+"""" aria-hidden="true">
                        <div class="modal-dialog modal-dialog-centered">
                            <div class="modal-content">
                                <div class="modal-body">
                                    <form action=" """ + reverse('adminin:add_noeud') + """ " class="m-1" method="get">
                                        <input type="hidden" name="id" value=" """ + str(node.id) + """ ">
                                        <div class="form-floating my-1">
                                            <input type="text" class="form-control rounded-0" name ="nom">
                                            <label for="nom"> nom du nouveau noeud </label>
                                        </div>
                                        <div class="form-floating my-1">
                                            <input type="text" class="form-control rounded-0" name ="question">
                                            <label for="question"> question du nouveau noeud </label>
                                        </div>
                                        <button type="submit" class="btn btn-primary m-1 border-0"><i class="fa fa-trash3"></i>valider</button>
                                    </form>
                                </div>
                            </div>
                        </div>
                    </div>
    
                """
    form_define_feuille = """
                        <button class="btn btn-primary w-100" data-bs-toggle="modal" data-bs-target="#___"""+str(node.id)+"""">
                            definir comme feuille
                        </button>
                        """
    modal_define_feuille = """
                         <div class="modal fade" id="___"""+str(node.id)+"""">
                            <div class="modal-dialog">
                              <div class="modal-content">
                                <div class="modal-body">
                                  <form action=" """ + reverse('adminin:form_leaf') + """" class="m-1" method="get" >
                                    <input type="hidden" name="id" value=" """ + str(node.id) + """ ">
                                        <div class="form-floating">
                                            <input type="number" class="form-control" name="nombre" >
                                            <label>nombre de caracteristiques</label>
                                        </div>
                                        <button type="submit" class="btn rounded-0 btn-primary border-0 m-1">valider</button>
                                    </form>
                                </div>
                              </div>
                            </div>
                        </div>
                         """
    if(n == 0):
        # on verifie si la feuille a deja ete defini comme feuille
        if len(Feuille.objects.filter(id=node.id)) != 0:
            return (""" <div class="d-flex align-items-center justify-content-between">
                             <div class="btn d-inline-flex align-items-center gap-2">
                                 <i class="fa fa-leaf"></i> """ + nom + """
                             </div>
                             <div class="btn-group">
                            <a type="button" class="fa fa-cog dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
                              </a>
                            <ul class="dropdown-menu dropdown-menu-right">
                              <li class="dropdown-item">"""+form_delete+"""</li>
                            </ul>
                        </div>
                         </div> """,
                        """"""
                )
        # construction de la vue d'une noeud terminal
        return (""" <div class="d-flex align-items-center justify-content-between">
                             <div class="btn d-inline-flex align-items-center ">
                                 <i class="fa fa-node"></i> """ + nom + """
                             </div>
                             <div class="btn-group">
                            <a type="button" class="fa fa-cog dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
                              </a>
                            <ul class="dropdown-menu dropdown-menu-right">
                              <li class="dropdown-item">"""+form_delete+"""</li>
                              <li class="dropdown-item">"""+form_add+"""</li>
                              <li class="dropdown-item">"""+form_define_feuille+"""</li>
                            </ul>
                        </div>
                         </div> """,
                         modal_add+modal_define_feuille
                         )

    # contruction du html noeud
    icon = """<i class="fa fa-chevron-right"></i> """ if node.parent != None else """<i class="fa fa-code-fork"></i> """
    result = """
            <ul class="list-unstyled m-0 py-1">
             <div class="d-flex align-items-center justify-content-between">
                <button class="btn d-inline-flex align-items-center collapsed rounded-0 gap-2" data-bs-toggle="collapse" data-bs-target="#_"""+str(node.id)+"""" aria-expanded="false">
                    """ + icon + nom + """
                </button>
                <div class="btn-group">
                <a type="button" class="fa fa-cog dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
                </a>
                    <ul class="dropdown-menu dropdown-menu-right">
                        <li class="dropdown-item">"""+form_delete+"""</li>
                        <li class="dropdown-item">"""+form_add+"""</li>
                        <li class="dropdown-item">"""+form_define_feuille+"""</li>
                    </ul>
                </div>
             </div> """

    # > insertion des enfants
    result += """ <div class="collapse border-start ps-2" id="_"""+str(node.id)+"""">
                    <ul class="list-unstyled">"""
    
    modals = modal_add+modal_define_feuille
    for child in children:
        res = node_tohtml(child)
        result += "<li>" + res[0] + "</li>"
        modals += res[1]
    result += "</ul></div></ul>"

    return (result, modals)

def generate_hierachie():
    trees_visual = ""
    racines = Noeud.objects.filter(parent=None)
    modals = ""
    if(len(racines) != 0):
        for racine in racines:
            res = node_tohtml(racine)
            modals += res[1]
            trees_visual += res[0]
        trees_visual += modals
    else:
        trees_visual = trees_visual + "<h2> Aucun noeud existant </h2>"
    return trees_visual
