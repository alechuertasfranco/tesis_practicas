from django.urls import path,include
# from gestionPracticas.views import 
from gestionPracticas.views import agregarPractica,save_Asesor,save_Empresa,save_Practica,listarPractica,verAsesor,asesor_practica,fetchAlumnoPractica,save_Visado
from django.contrib.auth import views
urlpatterns = [
  # path('', acceder,name="login"),
  # path('home/',homePage ,name="home"),
    path('agregarPractica',agregarPractica,name="agregarPractica"),
    path('save_Empresa',save_Empresa,name="save_Empresa"),
    path('save_Visado',save_Visado,name="save_Visado"),
    path('asesor_practica',asesor_practica,name="asesor_practica"),
    path('verAsesor/<int:id>/',verAsesor,name="verAsesor"),
    path('fetchAlumnoPractica/<int:id>/',fetchAlumnoPractica,name="fetchAlumnoPractica"),
    path('save_Practica',save_Practica,name="save_Practica"),
    path('save_Asesor',save_Asesor,name="save_Asesor"),
    path('listarPractica',listarPractica,name="listarPractica"),
]