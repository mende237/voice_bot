from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from voiceBot import settings
from django.core.mail import EmailMessage, send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from . tokens import generate_token
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str , force_text
from enseignant.models import Enseignant

def welcome(request):
    return render(request ,"authentification/welcome.html")

def error(request):
    return render(request ,"authentification/connectionerror.html")

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['password']
        pass2 = request.POST['re_password']
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('error')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('error')
        
        if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('error')
        
        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('error')
        
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('error')

        myUser  = User.objects.create_user(username ,email ,pass1)
        myUser.first_name = fname
        myUser.last_name = lname
        myUser.is_active= False
        myUser.save()
        messages.success(request , "Your account has been succefully create")

        # Welcome Email
        subject = "Welcome to EasyInformation Admin!!"
        message = "Hello " + myUser.first_name + "!! \n" + "Your password is :"+pass1  +" Welcome to EasyInformation!! \nThank you for visiting our website\n. We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\n"        
        from_email = settings.EMAIL_HOST_USER
        to_list = [myUser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        
        # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email @ EasyInformation - Login system!!"
        message2 = render_to_string('email_confirmation.html',{
            
            'name': myUser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myUser.pk)),
            'token': generate_token.make_token(myUser)
        })
        email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [myUser.email],
        )
        email.fail_silently = True
        try:
            email.send()
        except:
            return render(request ,"authentification/connectionerror.html")
        
        return redirect('admin:home')
    return render(request ,"authentification/signup.html")



def addTeacher(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['password']
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('error')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('error')
        
        if len(username) ==0:
            messages.error(request, "Username must be not null!!")
            return redirect('error')

        myUser  = User.objects.create_user(username ,email ,pass1)
        h = Enseignant()
        h.email = email
        h.set_password(pass1)
        h.username  = username
        h.save()
        myUser.is_active= False
        myUser.save()
        messages.success(request , "Your account has been succefully create")

        # Welcome Email
        subject = "Welcome to EasyInformation Admin!!"
        message = "Hello " + myUser.username + "!! \n" + "Your password is :"+pass1  +" Welcome to EasyInformation!! \nThank you for visiting our website\n. We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\n"        
        from_email = settings.EMAIL_HOST_USER
        to_list = [myUser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        
        # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email @ EasyInformation - Login system!!"
        message2 = render_to_string('email_confirmation.html',{
            
            'name': myUser.username,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myUser.pk)),
            'token': generate_token.make_token(myUser)
        })
        email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [myUser.email],
        )
        email.fail_silently = True
        try:
            email.send()
        except:
            return render(request ,"authentification/connectionerror.html")
        
        return redirect('admin:home')
    return render(request ,"authentification/addTeacher.html")



def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['password']
        
        user = authenticate(username=username, password=pass1)
        print(user)
        if user is  None:
            messages.error(request, "Error during authentification")
            return redirect('signin')
        else:
            login(request, user)
            fname = user.first_name
            messages.success(request, "Logged In Sucessfully!!")
            #return render(request, "authentification/index.html",{"fname":fname})
            request.session['fname'] = fname
            return redirect('administration:Home')
    return render(request, "authentification/signin.html")



def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('signin')
 



def signinTeacher(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['password']
        
        if(Enseignant.objects.filter(name=username) and Enseignant.objects.filter(password=pass1) and Enseignant.objects.filter(email=email)):
            messages.success(request, "Logged In Sucessfully!!")
            request.session['name'] = username
            return redirect('enseignant:view_tree')
        else :
            messages.error(request, "Error during authentification")
            return redirect('signinTeacher')
    return render(request, "authentification/signinTeacher.html")



def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('signin')
 

def activate(request,uidb64,token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        #myuser.profile.signup_confirmation = True
        myuser.save()
        login(request,myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('signin')
    else:
        return render(request,'activation_failed.html')


def admin(request):
    return render(request , 'home.html')

def ajouterEnseignant(request):
   # ens = Enseignant()
    if request.method == "POST":
        name = request.POST['name']
        password = request.POST['password']

        
    return render(request ,'enseignant/ajouter.html')