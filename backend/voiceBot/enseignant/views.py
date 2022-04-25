import datetime
from administration.models import Caracteristique
from enseignant.models import Enseignant, Information, ValCaracteristique
from django.shortcuts import redirect, render, get_object_or_404



# Create your views here.
def ajouter_information(request):
    id = 2
    date = datetime.datetime.strptime(
        request.GET['delai'], "%Y-%m-%d")
    
    enseignant = get_object_or_404(Enseignant, pk=id)
    info = Information(delai=date, enseignant=enseignant)    
    info.save()
    
    for r in request.GET:
        if r != 'delai':
            val = ValCaracteristique(
                content=request.GET[r],information = info, caracteristique = get_object_or_404(Caracteristique , pk = int(r)))
            val.save()
    return redirect('enseignant:view_form')

def view_form(request):
    html_form = ""
    id = 15

    infos = Information.objects.filter(valcaracteristique__caracteristique__feuille__id = id)
    # for info in infos:
    #     if info.delai > datetime.date.today():
    #         return render(request, 'fill.html')
        
    #print("enter*********************************************************************")
    caracteristiques = Caracteristique.objects.filter(feuille_id=id)
    for caracteristique in caracteristiques:
        html_form += make_input(caracteristique) + "<br>" 
    
    html_form += """ 
                 <div class = "mb-3 row" ><label for = "staticEmail" class = "col-sm-2 col-form-label"> delai </label >
                     <div class = "col-sm-10">
                         <input type = "date" name = "delai"> 
                     </div >
                 </div> 
                 <div class = "col-auto" >
                       <button type = "submit" class = "btn btn-primary mb-3" > Confirm </button >
                 </div> 
                 """
    print("test***********************************************************************************")
    # fichier = open("templates/test.html", "w")
    # fichier.write(html_form)
    # fichier.close()
    return render(request, 'fill.html', context={"html_form": html_form})

def edit_info(request):
    
    pass




def make_input(caracteristique):
    type = ''
    if caracteristique.type == '2' or caracteristique.type == '3':
        type = 'number'
    elif caracteristique.type == '4':
        type = 'text'
    else:
        type = 'date'
        
   
    result = """<div class = "mb-3 row" ><label for = "staticEmail" class = "col-sm-2 col-form-label"> """ + caracteristique.nom + """ </label >
                    <div class = "col-sm-10">
                        <input type = " """ + type + """" name = " """ + str(caracteristique.id) + """ " """ + """> 
                    </div >
                </div>"""
    return result
    
