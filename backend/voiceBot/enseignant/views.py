import datetime
from administration.models import Caracteristique
from enseignant.models import Enseignant, Information, ValCaracteristique
from django.shortcuts import redirect, render, get_object_or_404

from enseignant.handle_teacher_tree import generate_hierachie



# Create your views here.
def ajouter_information(request):
    email = request.session['email']
    print(f"l'email est {email}")
    id = Enseignant.objects.get(email = email).id
    print(f"l'identifiant est {id}")
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
    return redirect('enseignant:view_tree')

def view_tree(request):
    hierarchie = generate_hierachie()
    return render(request, "homeTeacher.html", {'hierarchie': hierarchie , "teacherName" : "null pour le moment"})

def view_form(request):
    html_form = ""
    id = request.GET['id']

    infos = Information.objects.filter(valcaracteristique__caracteristique__feuille__id = id)
    for info in infos:
        if info.delai > datetime.date.today():
            return render(request, 'fill.html')
        
    #print("enter*********************************************************************")
    caracteristiques = Caracteristique.objects.filter(feuille_id=id)
    for caracteristique in caracteristiques:
        html_form += make_input(caracteristique) + "<br>" 
    
    html_form += """ 
                 <div class = "mb-3 row" ><label for = "staticEmail" class = "col-sm-2 col-form-label"> Expiration  date</label >
                     <div class = "col-sm-10">
                         <input type = "date" name = "delai"> 
                     </div >
                 </div> 
                 <div class = "col-auto" >
                       <button type = "submit" class = "btn btn-primary mb-3" > Confirm </button >
                 </div> 
                 """
    return render(request, 'fill.html', context={"html_form": html_form})

def edit_info(request):
    
    pass




def make_input(caracteristique):
    type = ''
    if caracteristique.type == '2' or caracteristique.type == '3':
        type = 'number'
    elif caracteristique.type == '4':
        type = 'text'
    elif caracteristique.type == '1':
        type = 'date'
    else:
        type = 'time'
        
    
    result = f"""<div class = "mb-3 row" ><label for = "staticEmail" class = "col-sm-2 col-form-label">{caracteristique.nom}</label >
                    <div class = "col-sm-10">
                        <input type = "{type}" name = "{str(caracteristique.id)}"> 
                    </div >
                </div>"""
    return result
    
def modify_info(request):
    if request.method == "POST" :
        username = request.POST['username']
        password = request.POST['password']
        file = request.POST['file']
        flag1 =0
        flag2 = 0
        flag3 = 0
        if len(username) =="":
            flag1 = 1
        if len(password) == 0:
            flag2  =1
        if len(file)==0:
            flag3 = 1
        
        

    return render(request , "modifyTeacherInfo.html")
