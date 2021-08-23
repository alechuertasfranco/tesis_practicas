from django.urls import path,include
from gestionSeguridad.views import home
from django.contrib.auth import views
urlpatterns = [
  # path('', acceder, name="login"),
  path('', home, name="home"),
]