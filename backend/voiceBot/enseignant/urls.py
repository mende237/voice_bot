from django.urls import path
from enseignant import views

urlpatterns = [
    path("add_noeud", views.ajouter_noeud,name='add_noeud'),
]