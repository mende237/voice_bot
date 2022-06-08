from django.urls import path
from enseignant import views

urlpatterns = [
    path("add_info", views.ajouter_information,name='add_info'),
    path("update_info", views.update_information, name='update_info'),
    path("view_form", views.view_form, name='view_form'),
    path("view_form_with_default_value", views.view_form_with_default_value,
         name='view_form_with_default_value'),
    path("view_tree", views.view_tree, name='view_tree'),
    path("modify_info" , views.modify_info , name ="modify_info")
]
