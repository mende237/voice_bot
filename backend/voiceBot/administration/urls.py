from django.urls import path
from administration import views

urlpatterns = [
    path("add_noeud", views.ajouter_noeud,name='add_noeud'),
    path("delete_noeud", views.delete_noeud,name='delete_noeud'),
    path("home", views.home, name="Home"),
]