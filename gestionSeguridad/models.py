from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Facultad(models.Model):
    descripcion = models.CharField(max_length=70)
    def __str__(self):
      return self.descripcion       
class Escuela(models.Model):
    facultad = models.ForeignKey(Facultad,on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=70)
    def __str__(self):
        return self.descripcion     
class Alumno(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nro_matricula = models.CharField(max_length=10)
    apellidos = models.CharField(max_length=40)
    nombres = models.CharField(max_length=40)
    email = models.EmailField()
    telefono = models.CharField(max_length=9)
    facultad = models.ForeignKey(Facultad,on_delete=models.SET_NULL,null=True)
    escuela = models.ForeignKey(Escuela,on_delete=models.SET_NULL,null=True)
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
    dni = models.CharField(max_length=8)
    email = models.EmailField()
    estado = models.BooleanField(default=True)
    def __str__(self):
      return self.nombres +" "+ self.apellidos
  
