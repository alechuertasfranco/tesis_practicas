from django.urls import path
from gestionTesis.views import *
from django.contrib.auth import views
urlpatterns = [
  path('tesis_estudiante/', index_estudiante, name="index_estudiante"),
  path('tesis_estudiante_error/', index_estudiante_error, name="index_estudiante_error"),
  path('tesis_jurado', index_jurado, name="index_jurado"),
  path('asignar_jurado', asignar_jurado, name="asignar_jurado"),
  path('tesis_secretaria/', index_secretaria, name="index_secretaria"),
]