from django.urls import path,include
# from gestionPracticas.views import 
from gestionPracticas.views import agregarPractica,save_Asesor,save_Empresa,save_Practica,listarPractica
from gestionPracticas.views import verAsesor,asesor_practica,fetchAlumnoPractica,save_Visado,secretaria_practica
from gestionPracticas.views import save_fechaPresentacion,save_informeFinal,info_plan,save_Resolucion
from django.contrib.auth import views
urlpatterns = [
  # path('', acceder,name="login"),
  # path('home/',homePage ,name="home"),
    path('agregarPractica',agregarPractica,name="agregarPractica"),
    path('save_Empresa',save_Empresa,name="save_Empresa"),
    path('save_Visado',save_Visado,name="save_Visado"),
    path('save_Resolucion',save_Resolucion,name="save_Resolucion"),
    path('save_informeFinal',save_informeFinal,name="save_informeFinal"),
    path('save_fechaPresentacion',save_fechaPresentacion,name="save_fechaPresentacion"),
    path('asesor_practica',asesor_practica,name="asesor_practica"),
    path('secretaria_practica',secretaria_practica,name="secretaria_practica"),
    path('verAsesor/<int:id>/',verAsesor,name="verAsesor"),
    path('info_plan/<int:id>/',info_plan,name="info_plan"),
    path('fetchAlumnoPractica/<int:id>/',fetchAlumnoPractica,name="fetchAlumnoPractica"),
    path('save_Practica',save_Practica,name="save_Practica"),
    path('save_Asesor',save_Asesor,name="save_Asesor"),
    path('listarPractica',listarPractica,name="listarPractica"),
]