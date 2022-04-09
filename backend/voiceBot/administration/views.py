from django.shortcuts import get_object_or_404, redirect, render
from matplotlib.style import context

from administration.models import Noeud

# Create your views here.
def ajouter_noeud(request):
    idParent = request.GET.get("parent")
    nom = request.GET.get("nom")
    if nom == None or nom == "" or nom[0] == " ":
        return redirect('administration:listeNode')
        
    new_node = Noeud(nom=nom)
    if idParent !=  None :
        parent = get_object_or_404(Noeud, pk=int(idParent))
        new_node.parent = parent
        

    new_node.save()
    print(nom)
    return redirect('administration:listeNode')
    
def indexNode(request):
    noeuds = Noeud.objects.all()
    print(noeuds)
    context={
        'noeuds' : noeuds,
    }
    return render(request, "node.html", context)
    
