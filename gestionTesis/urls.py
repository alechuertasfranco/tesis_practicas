from django.urls import path
from gestionTesis.views import *
from django.contrib.auth import views
urlpatterns = [
  path('tesis_estudiante/', index_estudiante, name="index_estudiante"),
  path('tesis_estudiante_error/', index_estudiante_error, name="index_estudiante_error"),
  path('tesis_docente', index_docente, name="index_docente"),
  path('modal_visar_tesis/<int:plan_id>/', visar_plan_tesis, name="visar_plan_tesis"),
  path('modal_observar_tesis/<int:observacion_id>/', observar_plan_tesis, name="observar_plan_tesis"),
  path('tesis_secretaria/', index_secretaria, name="index_secretaria"),
]