from django.contrib import admin

from administration.models import Caracteristique, Feuille
from enseignant.models import Enseignant, Information, ValCaracteristique

# Register your models here.
admin.site.register(Feuille)
admin.site.register(ValCaracteristique)
admin.site.register(Caracteristique)
admin.site.register(Enseignant)
admin.site.register(Information)
