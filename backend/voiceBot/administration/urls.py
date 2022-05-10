from django.urls import path
from administration import views

urlpatterns = [
    path("add_teacher" , views.add_teacher , name="add_teacher"),
    path("add_admin" , views.add_admin , name="add_admin"),
    path("add_noeud", views.ajouter_noeud,name='add_noeud'),
    path("create_leaf", views.create_leaf,name='create_leaf'),
    path("form_leaf", views.form_leaf,name='form_leaf'),
    path("delete_noeud", views.delete_noeud,name='delete_noeud'),
    path("home", views.home, name="Home"),
]