from django.urls import path
from administration import views

urlpatterns = [
    path("add_noeud", views.ajouter_noeud,name='add_noeud'),
    path("nodes", views.indexNode, name="listeNode"),
    path("home", views.home, name="Home"),
]