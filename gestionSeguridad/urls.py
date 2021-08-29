from django.contrib import admin
from django.urls import path
from gestionSeguridad.views import acceder,homePage,salir,listaralumno,agregaralumno,editaralumno,eliminaralumno,listardocente,agregardocente,editardocente,eliminardocente
from django.contrib.auth import views

urlpatterns = [
    path('',acceder,name="login"),
    path('home/',homePage,name="home"),
    path('logout/',salir,name="logout"),
    #alumnos
    path('listaralumno/',listaralumno,name="listaralumno"),
    path('agregaralumno/',agregaralumno,name="agregaralumno"),    
    path('editaralumno/<int:id>/',editaralumno,name="editaralumno"),    
    path('eliminaralumno/<int:id>/',eliminaralumno,name="eliminaralumno"),        
    #docentes
    path('listardocente/',listardocente,name="listardocente"),
    path('agregardocente/',agregardocente,name="agregardocente"),    
    path('editardocente/<int:id>/',editardocente,name="editardocente"),    
    path('eliminardocente/<int:id>/',eliminardocente,name="eliminardocente"),  
]
