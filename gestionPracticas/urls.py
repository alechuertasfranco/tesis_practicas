from django.urls import path,include
# from gestionPracticas.views import 
from gestionPracticas.views import agregarPractica,save_Asesor,save_Empresa,save_Practida,listarPractica,listarPractica_id,listarPractica_aceptado
from django.contrib.auth import views
urlpatterns = [
  # path('', acceder,name="login"),
  # path('home/',homePage ,name="home"),
    path('agregarPractica/<int:id>/',agregarPractica,name="agregarPractica"),
    path('save_Empresa',save_Empresa,name="save_Empresa"),
    path('save_Asesor',save_Asesor,name="save_Asesor"),
    path('listarPractica',listarPractica,name="listarPractica"),
    path('listarPractica_id',listarPractica_id,name="listarPractica_id"),
    path('listarPractica_aceptado',listarPractica_aceptado,name="listarPractica_aceptado"),
]