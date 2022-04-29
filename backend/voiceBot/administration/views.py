from django.shortcuts import get_object_or_404, redirect, render

from administration.models import Feuille, Noeud

def home(request):
    generate_hierachie()
    return render(request, "home.html")

def ajouter_noeud(request):
    idParent = request.GET.get("id")
    nom = request.GET.get("nom")
    if nom == None or nom == "" or nom[0] == "":
        return redirect('administration:Home')
        
    new_node = Noeud(nom=nom)
    if idParent !=  None :
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
    nom = "<h5 class=\"m-0\">"+ node.nom +"</h5>"
    result = ""
    
    form_delete = "<form action=\"{% url 'adminin:delete_noeud' %}\" class=\"m-1\" method=\"get\">" 
    form_delete = form_delete + "   <input type=\"hidden\" name=\"id\" value=" + str(node.id) +">"
    form_delete = form_delete + "   <button type=\"submit\" class=\" btn rounded-0 btn-outline-danger border-0\"><i class=\"fa fa-trash3\"></i> delete </button>"
    form_delete = form_delete + "</form>"
    
    form_add = "<form action=\"{% url 'adminin:add_noeud' %}\" class=\"m-1 d-flex\" method=\"get\">"
    form_add = form_add + "   <input type=\"hidden\" name=\"id\" value=" + str(node.id) +">"
    form_add = form_add + "   <label for=\"nom\" class=\"visually-hidden\"> nom </label><input type=\"text\" class=\"form-control rounded-0\" name =\"nom\">"
    form_add = form_add + "   <button type=\"submit\" class=\"btn rounded-0 btn-primary border-0\"><i class=\"fa fa-trash3\"></i>add</button>"
    form_add = form_add + "</form>"
    
    form_define_feuille = "<form action=\"#\" class=\"m-1\" method=\"get\" >"
    form_define_feuille = form_define_feuille + "   <input type=\"hidden\" name=\"id\" value=" + str(node.id) +" >"
    form_define_feuille = form_define_feuille + "   <button type=\"submit\" class=\"btn rounded-0 btn-outline-primary border-0\"><i class=\"fa fa-trash3\"></i>define leaf</button>"
    form_define_feuille = form_define_feuille + "</form>"
    
    if(n==0):
        # on verifie si la feuille a deja ete defini comme feuille
        if len(Feuille.objects.filter(id=node.id)) != 0 :
        
            # construction de la vue d'une feuille     
            result = result + " <div class=\"d-flex align-items-center justify-content-between\">"
            result = result + "     <div class=\"btn d-inline-flex align-items-center \">"
            result = result + "         <i class=\"fa fa-leaf\"></i>" + nom
            result = result + "     </div>"
            result = result + "     <div class=\"d-flex text-center mx-2 bg-light\">"+form_delete+"</div>"
            result = result + " </div>"
            return result
        
        result = result + " <div class=\"d-flex align-items-center justify-content-between\">"
        result = result + "     <div class=\"btn d-inline-flex align-items-center border-0 rounded-0\">"
        result = result + "         <i class=\"fa fa-node\"></i>" + nom
        result = result + "     </div>"
        result = result + "     <div class=\"d-flex text-center mx-2 bg-light\">"+form_delete+form_add+form_define_feuille+"</div>"
        result = result + " </div>"
        
        # construction de la vue d'une noeud terminal 
        return result
        
    ## contruction du html noeud
    result = result + "<ul class=\"list-unstyled m-0 py-1\">"
    result = result + " <div class=\"d-flex align-items-center justify-content-between \">"
    result = result + "     <button class=\"btn d-inline-flex align-items-center collapsed rounded-0 gap-2\" data-bs-toggle=\"collapse\" data-bs-target=\"#__"+str(node.id)+node.nom+"\" aria-expanded=\"false\">"
    result = result + "         <i class=\"fa fa-chevron-right\"></i>" + nom
    result = result + "     </button>"
    result = result + "     <div class=\"d-flex text-center mx-2 bg-light\">"+form_delete+form_add+form_define_feuille+"</div>"
    result = result + " </div>"
    
    #> insertion des enfants
    result = result + " <div class=\"collapse border-start ps-2\" id=\"__"+str(node.id)+node.nom+"\">"
    result = result + "     <ul class=\"list-unstyled\">"
    for child in children:
        result = result + "     <li>"
        result = result + node_tohtml(child)
        result = result + "     </li>"
    result = result + "     </ul>"
    result = result + " </div>"
    result = result + "</ul>"
    return result
    
def generate_hierachie():
    trees_visual = "{% load static %}\n"
    racines = Noeud.objects.filter(parent=None)
    
    if(len(racines)!=0):
        for racine in racines:
            trees_visual = trees_visual + node_tohtml(racine)
    else:
        trees_visual = trees_visual + "<h2> Aucun noeud existant </h2>"
    
    # sauvegerde dans le template associe de l'hierarchie
    fichier = open("templates/hierarchie_for_admin.html", "w")
    fichier.write(trees_visual)
    fichier.close()