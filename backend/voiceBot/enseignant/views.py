import datetime
from administration.models import Caracteristique , Feuille
from enseignant.models import Enseignant, Information, ValCaracteristique
from django.shortcuts import redirect, render, get_object_or_404
from enseignant.handle_teacher_tree import generate_hierachie


# Create your views here.
def ajouter_information(request):
    email = request.session['email']
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


def update_information(request):
    email = request.session['email']
    id_ens = Enseignant.objects.get(email=email).id
    print(f"l'identifiant est {id_ens}")
    id_info = request.GET['id_info']

    info = get_object_or_404(Information, pk=id_info)
    if info.enseignant_id == id_ens:
        nbr_car = request.GET['nbr_car']
        print("le nombre de caracteristique est :" + nbr_car)
        for i in range(int(nbr_car)):
            val_car_name = "val_car" + str(i+1)
            val_car_id = request.GET[val_car_name]
            type = request.GET["car"+val_car_id]
            content = request.GET[val_car_id]
            valeur_caracteristique = get_object_or_404(ValCaracteristique, pk=int(val_car_id))
            
            if type == '2':
                #number
                valeur_caracteristique.content = int(content)
            elif type == '3':
                #reel
                valeur_caracteristique.content = float(content)
            elif type == '4':
                #text
                valeur_caracteristique.content = content
            elif type == '1':
                #date
                print("date******************************")
                valeur_caracteristique.content = datetime.datetime.strptime(content, "%Y-%m-%d")
            else:
                #time
                valeur_caracteristique.content = datetime.datetime.strptime(content, "%H-%M-%S")
                
        valeur_caracteristique.save()
        delai = datetime.datetime.strptime(request.GET['delai'], "%Y-%m-%d")
        info.delai = delai
        info.save()
    #un enseignant ne peut pas modifier une information dont ce n'est pas lui l'auteur
    else:
        pass

    return redirect('enseignant:view_tree')

def view_tree(request):
    hierarchie = generate_hierachie()
    name =request.session['name']
    email = request.session['email']
    image =  Enseignant.objects.get(email = email).image
    print(image)
    return render(request, "homeTeacher.html", {'hierarchie': hierarchie , "teacherName" : name , "image":image })


def view_form(request):
    html_form = ""
    decision = request.GET['add_or_modif']
    if decision == 'ajouter':
        id = request.GET['id']
        sheet_name = ""
        sheets = Feuille.objects.filter(id = id)
        sheet_name = sheets[0].nom
        caracteristiques = Caracteristique.objects.filter(feuille_id=id)
        for caracteristique in caracteristiques:
            html_form += make_input(caracteristique) 
        
        return render(request, 'enseignant/fill.html', context={"html_form": html_form , "sheet_name":sheet_name})
        
    elif decision == 'modifier':
        return view_form_with_default_value(request)
        
    


def view_form_with_default_value(request):
    html_form = ""
    id_info = request.GET['id']
    html_form = ""
    sheet_name = ""
    
    sheets = Feuille.objects.filter(
        caracteristique__valcaracteristique__information_id=id_info)
    sheet_name = sheets[0].nom
    
    print("le nom de la feuille est {} le nombre de feuille est {} ".format(sheet_name , len(sheets)))
    infos = Information.objects.filter(id=id_info)
    delai = infos[0].delai

    val_caracteristiques = ValCaracteristique.objects.filter(
        information_id=id_info)
    
    cmpt = 0
    for val_caracterique in val_caracteristiques:
        caracteristiques = Caracteristique.objects.filter(id=val_caracterique.caracteristique_id)
        cmpt = cmpt + 1
        html_form += make_input(caracteristiques[0], val_caracterique , cmpt)
        
    
    
    return render(request, 'enseignant/edit_info.html', context={"html_form": html_form , "delai": str(delai) , "sheet_name":sheet_name , "nbr_car":len(val_caracteristiques) , "id_info":id_info})


def make_input(caracteristique , val_caracteristique = None , cmpt = 0):
    type = ''
    if caracteristique.type == '2' or caracteristique.type == '3':
        type = 'number'
    elif caracteristique.type == '4':
        type = 'text'
    elif caracteristique.type == '1':
        type = 'date'
    else:
        type = 'time'
    result = ""
    if val_caracteristique == None:
        result = f"""<tr>
                        <td><label for = "staticEmail" class = "sm-2 form-label">{caracteristique.nom}</label ></td>
                        <td><input class="form-control" type = "{type}" name = "{str(caracteristique.id)}" required="required"></td>
                    </tr>"""
    else:
        val_car_name = "val_car" + str(cmpt)
        print(val_car_name)
        car_name = "car" + str(val_caracteristique.id)
        result = f"""<tr>
                        <td><label for = "staticEmail" class = "sm-2 form-label">{caracteristique.nom}</label ></td>
                        <td>
                            <input type = "hidden" name = "{val_car_name}" value = "{val_caracteristique.id}" >
                            <input type = "hidden" name = "{car_name}" value = "{caracteristique.type}" >
                            <input class="form-control" type = "{type}" name = "{val_caracteristique.id}" value = "{val_caracteristique.content}" required="required">
                        </td>
                    </tr>"""
                    
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
