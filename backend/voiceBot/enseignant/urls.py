from django.urls import path
from enseignant import views

urlpatterns = [
    path("add_info", views.ajouter_information,name='add_info'),
    path("view_form", views.view_form, name='view_form'),
    path("view_tree", views.view_tree, name='view_tree'),
    path("modify_info" , views.modify_info , name ="modify_info")
]
