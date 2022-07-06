from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from voiceBot import settings   
from django.core.mail import EmailMessage, send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from authentification.tokens import generate_token
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str, force_text
from enseignant.models import Enseignant

from django.core import serializers
from administration.models import TYPE_CHOICES, Administrateur, Caracteristique, Feuille, Formulation, Noeud
from administration.utils import *


def home(request):
    hierarchie = generate_hierachie()
   # print(request.session["fname"])
    return render(request, "home.html", {'hierarchie': hierarchie, 'active_admin_load': "active"})


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
                <input type="text" class="form-control" name="nom_""" + str(i) + """">
            </td>
            <td>
                <select class="form-select form-control form-select-sm" name="type_""" + str(i) + """" id="">
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
        'inputs': inputs,
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


def modif_noeud(request):
    id = request.GET.get("id")
    nom = request.GET.get("nom")
    if nom == None or nom == "" or nom[0] == "":
        return redirect('administration:Home')

    question = request.GET['question']
    noeud = get_object_or_404(Noeud, pk=int(id))
    noeud.question =question
    noeud.nom =nom
    noeud.save()
    return redirect('administration:Home')


def delete_noeud(request):
    id = request.GET.get("id")
    node = get_object_or_404(Noeud, pk=int(id))
    node.delete()
    generate_hierachie()
    return redirect('administration:Home')


def add_admin(request):
    return render(request, "add_anotherAdmin.html")


def form_format_formulation(request):
    id = int(request.GET["id"])
    feuille = get_object_or_404(Feuille, pk=id)
    carateristiques = Caracteristique.objects.filter(feuille=feuille)

    choises = ""
    for car in carateristiques:
        choises += """<option value = ' """ + \
            str(car.id) + """  '> """ + car.nom + """ </option> """

    context = {
        "id_feuille": id,
        "choises": choises,
        "data": 'i',
    }
    return render(request, "format_formulation.html", context)


def add_format_formulation(request):
    id = int(request.GET["id_feuille"])
    feuille = get_object_or_404(Feuille, pk=id)
    ind = 0
    ok = True
    ids_caracteristique = []
    while ok:
        num_id = request.GET.get("feature_"+str(ind))
        ind += 1
        if num_id == None:
            ok = False
        else:
            ids_caracteristique.append(num_id)
    format_formulation = request.GET["format"]
    form = Formulation(format_formulation=format_formulation,
                       caracteristiques=";".join(ids_caracteristique), feuille=feuille)
    form.save()
    return redirect("administration:Home")


def add_admin(request):
    return render(request, "add_anotherAdmin.html")


def add_teacher(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['password']
        h = Enseignant()
       # myUser  = User.objects.create_user(username ,email ,pass1)
        if Enseignant.objects.filter(name=username):
            messages.error(
                request, "Username already exist! Please try some other username.")
            return redirect('error')

        if Enseignant.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('error')

        h.email = email
        h.password = pass1
        h.name = username
        h.save()

        messages.success(request, "Your account has been succefully create")

        # Welcome Email
        subject = "Welcome to EasyInformation Teacher!!"
        message = "Hello " + h.name + "!! \n" + "Your password is :"+pass1 + \
            " Welcome to EasyInformation!! \nThis is your information to administrate system\n. We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\n"
        from_email = settings.EMAIL_HOST_USER
        to_list = [h.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email @ EasyInformation - Login system!!"
        message2 = render_to_string('email_confirmation.html', {

            'name': h.name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(h.id)),
            'token': generate_token.make_token(h)
        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [h.email],
        )
        email.fail_silently = True
        try:
            email.send()
        except:
            return render(request, "authentification/connectionerror.html")

        print("ajout reussi")
        return redirect('administration:Home')
    return render(request, "add_Teacher.html")

# vue pour voir tous les administrateurs


def account_ens(request):
    enss = Enseignant.objects.all()
    context = {'enss': enss, 'active_admin_ens': "active"}
    return render(request, "admin/account_ens.html", context)

# vue pour voir tous les enseignants


def account_admin(request):
    admins = Administrateur.objects.all()
    context = {'admins': admins, 'active_admin_account': "active"}
    return render(request, "admin/account_admin.html", context)

# action de suppresion d'un administrateur


def delete_admin(request, id):
    admin = get_object_or_404(Administrateur, pk=int(id))
    admin.delete()
    return redirect('administration:account_admin')

# action de suppression d'un enseignant


def delete_ens(request, id):
    ens = get_object_or_404(Enseignant, pk=int(id))
    ens.delete()
    return redirect('administration:account_ens')

# vue de modification d'une feuille


def modifier_feuille_vue(request, id_feuille):
    feuille = get_object_or_404(Feuille, pk=int(id_feuille))
    cars_f = Caracteristique.objects.filter(feuille=feuille)

    cars = []
    for car in cars_f:
        type_ = ""
        if car.type == "1":
            type_ = "Date"
        elif car.type == "2":
            type_ = "Entier"
        elif car.type == "3":
            type_ = "Réel"
        elif car.type == "4":
            type_ = "Chaine de caratère"

        cars.append({'nom': car.nom, 'type': type_, 'id': car.id})

    context = {'cars': cars, 'active_admin_load': "active", "id_feuille": int(
        id_feuille), 'nom': feuille.nom, 'description': feuille.description, "choices": TYPE_CHOICES}
    return render(request, 'admin/modif_feuille.html', context)

# action de suppression d'une feuille


def modifier_feuille(request):
    id_feuille_ = int(request.GET.get("id_feuille"))
    feuille = get_object_or_404(Feuille, pk=id_feuille_)
    nom = request.GET.get("nom")
    description = request.GET.get("description")

    feuille.nom = nom
    feuille.description = description

    feuille.save()
    return redirect('administration:Home')

# action de suppresion de caracteristiques


def delete_caracteristique(request, id_feuille, id_car):
    feuille = get_object_or_404(Feuille, pk=int(id_feuille))
    cars_f = Caracteristique.objects.filter(feuille=feuille)
    if len(cars_f) > 1:
        car = get_object_or_404(Caracteristique, pk=int(id_car))
        car.delete()
    return redirect('administration:modifier_feuille_vue', id_feuille=int(id_feuille))

# action de modificataion d'une caracteristique


def modif_caracteristique(request):
    id_feuille = int(request.GET.get("id_feuille"))
    id_car = int(request.GET.get("id_car"))
    nom = request.GET.get("nom")
    type = request.GET.get("type")
    car = get_object_or_404(Caracteristique, pk=int(id_car))
    car.nom = nom
    car.type = type
    car.save()
    return redirect('administration:modifier_feuille_vue', id_feuille=int(id_feuille))

# action d'ajout d'une caracterisque


def ajouter_caracteristique(request):
    id_feuille = int(request.GET.get("id_feuille"))
    feuille = get_object_or_404(Feuille, pk=id_feuille)
    nom = request.GET.get("nom")
    type = request.GET.get("type")
    car = Caracteristique(nom=nom, type=type, feuille=feuille)
    car.save()
    return redirect('administration:modifier_feuille_vue', id_feuille=int(id_feuille))
