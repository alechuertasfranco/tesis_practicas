from django.db import models

# Create your models here.
class Alumno(models.Model):
    nombre = models.CharField(max_length=40)
    apellidos = models.CharField(max_length=40)
    email = models.EmailField()
    dni = models.CharField(max_length=8)
    estado = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre

class Docente(models.Model):
    nombre = models.CharField(max_length=40)
    apellidos = models.CharField(max_length=40)
    email = models.EmailField()
    dni = models.CharField(max_length=8)
    estado = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre