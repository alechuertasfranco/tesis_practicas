from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Alumno(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nro_matricula = models.CharField(max_length=10)
    apellidos = models.CharField(max_length=40)
    nombres = models.CharField(max_length=40)
    email = models.EmailField()
    telefono = models.CharField(max_length=9)
    facultad = models.CharField(max_length=40)
    escuela = models.CharField(max_length=40)
    ciclo_academico = models.CharField(max_length=4)
    estado = models.BooleanField(default=True)
    def __str__(self):
      return self.nombres +" "+ self.apellidos

class Docente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    apellidos = models.CharField(max_length=40)
    nombres = models.CharField(max_length=40)
    titulo = models.CharField(max_length=5)
    telefono = models.CharField(max_length=9)
    email = models.EmailField()
    estado = models.BooleanField(default=True)
    def __str__(self):
      return self.nombres +" "+ self.apellidos