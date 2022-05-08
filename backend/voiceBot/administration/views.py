from django.shortcuts import get_object_or_404, redirect, render
from django.core import serializers

from administration.models import Caracteristique, Feuille, Noeud
from administration.utils import generate_hierachie


def home(request):
    hierarchie = generate_hierachie()
    return render(request, "home.html" , { 'hierarchie' : hierarchie} )


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
    context = {
        'nombre':  int(nombre),
        'nom': node.nom,
        'id': id,
        'inputs' : inputs,
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

def add_admin(request):
    return render(request , "add_anotherAdmin.html")

def form_format_formulation(request):
    id = int(request.GET["id"])
    feuille = get_object_or_404(Feuille, pk=id)
    carateristiques = Caracteristique.objects.filter(feuille = feuille)
    
    choises = ""
    for car in carateristiques :
        choises += """<option value = ' """+ str(car.id) +"""  '> """+ car.nom +""" </option> """
        
    context = {
        "id_feuille": id,
        "choises": choises,
        "data" : 'i',
    }
    return render(request, "format_formulation.html", context)
    
def add_format_formulation(request):
    id = int(request.GET["id_feuille"])
    feuille = get_object_or_404(Feuille, pk=id)
    
    ind = 0
    ok = True
    ids_caracteristique = []
    while ok:
        num_id = request.GET["feature_"+(ind)]
        ind += 1
        if num_id == None :
            ok = False
        else :
            ids_caracteristique.append(int(num_id))
            
    format_formulation = request.GET["format"]
    
    
    return ""