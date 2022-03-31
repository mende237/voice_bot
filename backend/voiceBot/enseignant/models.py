from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User
from administration.models import Caracteristique

class Enseignant (User):
    matricule = models.CharField(max_length=10, unique=True)
    image = models.ImageField(upload_to="uploads/user/ens/", blank=True)
    def ajouter_info(information):
        pass
    
class Information(models.Model):
    delai = models.DateField('date limite de validite')
    enseignant = models.ForeignKey(Enseignant,  on_delete=models.CASCADE)
    
    
class ValCaracteristique(models.Model):
    content = models.CharField(max_length=30)
    caracteristique = models.ForeignKey(Caracteristique, on_delete = models.CASCADE)
    

    