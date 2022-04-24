from django.shortcuts import get_object_or_404, redirect, render

from administration.models import Caracteristique, Feuille, Noeud


def home(request):
    generate_hierachie()
    return render(request, "home.html")


def create_leaf(request):
    id = request.GET['id']
    nombre = request.GET['nombre']
    nombre = int(nombre)
    if id == "":
        # si il n'ya pas d'identifiant definie alors ca signifie qu'on veut creer une nouvelle feuille
        id_parent = int(request.GET['id_parent'])

        # on verifie s'il ya un parent
        bac = Noeud.objects.filter(id=id_parent)
        parent = None
        if len(bac) != 0:
            parent = bac[0]

        # on cree la feuille
        feuille = Feuille(
            nom=request.GET['nom'], description=request.GET['description'], parent=parent)
        feuille.save()
        for i in range(nombre):
            c = Caracteristique(
                nom=request.GET["nom_"+str(i)], type=request.GET["type_"+str(i)], feuille=feuille)
            c.save()

    else:
        id = int(id)
        node = get_object_or_404(Noeud, pk=id)
        feuille = Feuille(pk=node.id, nom=node.nom,
                          description=request.GET['description'], parent=node.parent)
        feuille.save()
        for i in range(nombre):
            c = Caracteristique(
                nom=request.GET["nom_"+str(i)], type=request.GET["type_"+str(i)], feuille=feuille)
            c.save()

    return redirect("administration:Home")


def form_leaf(request):
    nombre = request.GET.get("nombre")

    if int(nombre) <= 0:
        return render(request, "home.html")

    inputs = ""
    id = request.GET.get("id")
    node = get_object_or_404(Noeud, pk=int(id))
    for i in range(int(nombre)):
        inputs += """
        <tr>
            <td>
                <input type="text" class="w-100" name="nom_""" + str(i) + """">
            </td>
            <td>
                <select class="form-select form-select-sm" name="type_""" + str(i) + """" id="">
                    <option value="1">Date</option>
                    <option value="2">Entier</option>
                    <option value="3">Reel</option>
                    <option value="4">Chaine de Caractere</option>
                </select>
            </td>
        </tr>
        """
    fichier = open("templates/inputs_leafs.html", "w")
    fichier.write(inputs)
    fichier.close()

    context = {
        'nombre':  int(nombre),
        'nom': node.nom,
        'id': id,
    }
    return render(request, "form_leaf.html", context)


def ajouter_noeud(request):
    idParent = request.GET.get("id")
    nom = request.GET.get("nom")
    if nom == None or nom == "" or nom[0] == "":
        return redirect('administration:Home')
        
    question = request.GET['question']
    new_node = Noeud(nom=nom, question=question)
    
    if idParent != "":
        parent = get_object_or_404(Noeud, pk=int(idParent))
        new_node.parent = parent

    new_node.save()
    return redirect('administration:Home')


def delete_noeud(request):
    id = request.GET.get("id")
    node = get_object_or_404(Noeud, pk=int(id))
    node.delete()
    generate_hierachie()
    return redirect('administration:Home')


def node_tohtml(node):
    children = node.noeud_set.all()
    n = len(children)
    nom = "<h5 class=\"m-0\">" + node.nom + "</h5>"

    form_delete = """   <form action="{% url 'adminin:delete_noeud' %}" class="m-1" method="get"> 
                           <input type="hidden" name="id" value=" """ + str(node.id) + """ ">
                           <button type="submit" class=" btn  btn-danger"><i class="fa fa-trash-o "></i></button>
                        </form>  """

    form_add = """  
                <div class="d-flex align-items-center m-1">
                    <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#___"""+str(node.id)+"""">
                        <i class="fa fa-plus "></i>
                    </button>
                    <div class="modal fade" id="___"""+str(node.id)+"""" aria-hidden="true">
                        <div class="modal-dialog modal-dialog-centered">
                            <div class="modal-content">
                                <div class="modal-body">
                                    <form action="{% url 'adminin:add_noeud' %}" class="m-1" method="get">
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
                </div>
                """

    form_define_feuille = """
                        <div class="d-flex align-items-center m-1">
                            <button type="button" class="btn btn-success" data-bs-toggle="modal" data-bs-target="#____"""+str(node.id)+"""">
                                <i class="fa fa-leaf "></i>
                            </button>
                            <div class="modal fade" id="____"""+str(node.id)+"""" aria-hidden="true">
                                <div class="modal-dialog modal-dialog-centered">
                                  <div class="modal-content">
                                    <div class="modal-body">
                                        <form action="{% url 'adminin:form_leaf' %}" class="m-1" method="get" >
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
                        </div>
                        """
    if(n == 0):
        # on verifie si la feuille a deja ete defini comme feuille
        if len(Feuille.objects.filter(id=node.id)) != 0:
            return """ <div class="d-flex align-items-center justify-content-between">
                             <div class="btn d-inline-flex align-items-center gap-2">
                                 <i class="fa fa-leaf"></i> """ + nom + """
                             </div>
                             <div class="d-flex text-center mx-2 bg-light"> """+form_delete+""" </div>
                         </div> """
        # construction de la vue d'une noeud terminal
        return """ <div class="d-flex align-items-center justify-content-between">
                             <div class="btn d-inline-flex align-items-center ">
                                 <i class="fa fa-node"></i> """ + nom + """
                             </div>
                             <div class="d-flex text-center mx-2 bg-light"> """+form_delete+form_add+form_define_feuille+""" </div>
                         </div> """

    # contruction du html noeud
    icon = """<i class="fa fa-chevron-right"></i> """ if node.parent != None else """<i class="fa fa-code-fork"></i> """
    result = """
            <ul class="list-unstyled m-0 py-1">
             <div class="d-flex align-items-center justify-content-between">
                <button class="btn d-inline-flex align-items-center collapsed rounded-0 gap-2" data-bs-toggle="collapse" data-bs-target="#__"""+str(node.id)+"""" aria-expanded="false">
                    """ + icon + nom + """
                </button>
                <div class="d-flex text-center mx-2 bg-light"> """+form_delete+form_add+form_define_feuille+"""</div>
             </div> """

    # > insertion des enfants
    result += """ <div class="collapse border-start ps-2" id="__"""+str(node.id)+"""">
                    <ul class="list-unstyled">"""

    for child in children:
        result += "<li>" + node_tohtml(child) + "</li>"
    result += "</ul></div></ul>"

    return result


def generate_hierachie():
    trees_visual = "{% load static %}\n"
    racines = Noeud.objects.filter(parent=None)

    if(len(racines) != 0):
        for racine in racines:
            trees_visual = trees_visual + node_tohtml(racine)
    else:
        trees_visual = trees_visual + "<h2> Aucun noeud existant </h2>"

    # sauvegerde dans le template associe de l'hierarchie
    fichier = open("templates/hierarchie_for_admin.html", "w")
    fichier.write(trees_visual)
    fichier.close()
