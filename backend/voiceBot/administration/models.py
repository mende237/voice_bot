from django.db import models
from django.contrib.auth.models import User

TYPE_CHOICES = (
    ('1','Date'),
    ('2','Entier'),
    ('3','Reel'),
    ('4','ChaineDeCaractere'),
)

class Noeud(models.Model):
    parent = models.ForeignKey('self', on_delete = models.CASCADE, null=True)
    nom = models.CharField(max_length=50)
    question = models.CharField(max_length=100, default="")
    def tohtml(self):
        pass
        
class Feuille(Noeud):
    description = models.TextField(max_length=500, blank=True)
    CHEMIN_FILE_FORMAT_FORMULATION = ""
    
     
class formulation(models.Model):
    format_formulation = models.CharField(max_length=400, blank=True)
    
    pass
    
class Caracteristique(models.Model):
    nom = models.CharField(max_length=50)
    type = models.CharField(max_length=2, choices = TYPE_CHOICES)
    feuille = models.ForeignKey(Feuille, on_delete=models.CASCADE)
    
        
class Administrateur(User):
    image = models.ImageField(upload_to="uploads/user/admin/", blank=True)
    
    
    


