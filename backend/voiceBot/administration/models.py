from django.db import models
from django.contrib.auth.models import User

TYPE_CHOICES = (
    ('1','Date'),
    ('2','Entier'),
    ('3','Reel'),
    ('4','ChaineDeCaractere'),
)
class Noeud(models.Model):
    parent = models.ForeignKey('self', on_delete = models.CASCADE, blank=True)
    nom = models.CharField(max_length=50)
     
class Feuille(Noeud):
    description = models.TextField(max_length=500, blank=True)
    CHEMIN_FILE_FORMAT_FORMULATION = ""
    
    def genration_format_Formulation(self):
        pass
        
    def genration_Formulaire(self):
        pass
        
    
class Caracteristique(models.Model):
    nom = models.CharField(max_length=50)
    type = models.CharField(max_length=2, choices = TYPE_CHOICES)
    feuille = models.ForeignKey(Feuille, on_delete=models.CASCADE)
    
    def get_format_sur_formulaire(self):
        pass
        
class Administrateur(User):
    image = models.ImageField(upload_to="uploads/user/admin/", blank=True)
    
    def ajouter_un_noued(nom):
        pass
        
    def supprimer_un_noeud(noeud):
        pass
        
    def definir_un_noeud_comme_feuille(noeud):
        pass
    
    def format_formulation(feuille, chaine, list_caracteristiques ):
        pass
        
    def ajouter_caracteristique(feuille, caracteristique ):
        pass
        
    def ajouter_ensignant(enseignant):
        pass
    
    


