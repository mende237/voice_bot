from django.urls import path
from administration import views

urlpatterns = [
    path("add_teacher" , views.add_teacher , name="add_teacher"),
    path("add_admin" , views.add_admin , name="add_admin"),
    path("add_noeud", views.ajouter_noeud,name='add_noeud'),
    path("modif_noeud", views.modif_noeud,name='modif_noeud'),
    
    path("create_leaf", views.create_leaf,name='create_leaf'),
    path("form_leaf", views.form_leaf,name='form_leaf'),
    path("delete_noeud", views.delete_noeud,name='delete_noeud'),
    path("account_ens", views.account_ens,name='account_ens'),
    path("account_admin", views.account_admin,name='account_admin'),
    path("delete_admin/<int:id>", views.delete_admin,name='delete_admin'),
    path("delete_ens/<int:id>", views.delete_ens,name='delete_ens'),
    path("form_format_formulation", views.form_format_formulation,name='form_format_formulation'),
    path("add_format_formulation", views.add_format_formulation,name='add_format_formulation'),
    path("home", views.home, name="Home"),
    
    path("modifier_feuille_vue/<int:id_feuille>", views.modifier_feuille_vue,name='modifier_feuille_vue'),
    path("modifier_feuille", views.modifier_feuille,name='modifier_feuille'),
    path("delete_caracteristique/<int:id_feuille>/<int:id_car>", views.delete_caracteristique,name='delete_caracteristique'),
    path("modif_caracteristique", views.modif_caracteristique,name='modif_caracteristique'),
    path("ajouter_caracteristique", views.ajouter_caracteristique,name='ajouter_caracteristique'),
]