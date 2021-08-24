from django.contrib import admin
from django.urls import path
from gestionSeguridad.views import acceder,homePage,salir,alumnos,asesores,jurados
from django.contrib.auth import views

urlpatterns = [
    path('',acceder,name="login"),
    path('home/',homePage,name="home"),
    path('logout/',salir,name="logout"),
    path('alumnos/',alumnos,name="alumnos"),
    path('asesores/',asesores,name="asesores"),
    path('jurados/',jurados,name="jurados"),
]
