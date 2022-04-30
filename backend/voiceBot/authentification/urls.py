from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [

    path('activate/<uidb64>/<token>', views.activate, name='activate'),
      path('', views.welcome ,name="welcome"),
       path('home/', views.home ,name="home"),
     path('signup/' , views.signup ,name ="signup"),
     path('signin/' , views.signin ,name ="signin"),
     path('signout/' , views.signout ,name ="signout"),
     path('adminis_home' , views.admin , name="dashbord"),
]
