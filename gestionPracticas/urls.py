from django.urls import path,include
# from gestionPracticas.views import 
from gestionPracticas.views import agregarPractica,agregarEmpresa,agregarAsesor,listarPractica
from django.contrib.auth import views
urlpatterns = [
  # path('', acceder,name="login"),
  # path('home/',homePage ,name="home"),
    path('agregarPractica',agregarPractica,name="agregarPractica"),
    path('agregarEmpresa',agregarEmpresa,name="agregarEmpresa"),
    path('agregarAsesor',agregarAsesor,name="agregarAsesor"),
    path('listarPractica',listarPractica,name="listarPractica"),

]