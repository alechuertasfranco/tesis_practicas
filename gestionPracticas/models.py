from typing import ClassVar
from django.db import models
from django.db.models import signals
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from gestionSeguridad.models import Alumno, Docente
# Create your models here.

class Empresa(models.Model):
    razon_social = models.CharField(max_length=100)
    ruc = models.CharField(max_length=11) 
    direccion = models.CharField(max_length=200)
    ciudad = models.CharField(max_length=30)
    gerente = models.CharField(max_length=100)
    telefono = models.CharField(max_length=9)
    estado = models.CharField(max_length=10, default="Activo")  

class Contacto(models.Model):
    nombres = models.CharField(max_length=50)
    cargo = models.CharField(max_length=50)
    telefono = models.CharField(max_length=9)
    email = models.CharField(max_length=50)
    estado = models.CharField(max_length=10, default="Activo")
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)      

class PlanPracticas(models.Model):
    fecha_tramite = models.DateField()
    derecho_tramite = models.FileField(upload_to="plan_practica/")
    plan_practicas = models.FileField(upload_to="plan_practica/")
    fecha_presentacion = models.DateField(null=True)
    informe_final = models.FileField(upload_to="plan_practicas/", null=True)
    resolucion = models.FileField(upload_to="plan_practicas/", null=True)
    estado = models.CharField(max_length=10, default="CREADO")
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    asesor = models.ForeignKey(Docente, on_delete=models.CASCADE)
    empresa= models.ForeignKey(Empresa, on_delete=models.CASCADE)
    contacto =  models.ForeignKey(Contacto, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        print('save() is called.')
        super(PlanPracticas, self).save(*args, **kwargs)

@receiver(pre_save, sender=PlanPracticas)
@receiver(post_save, sender=PlanPracticas)
def reicever(*args, **kwargs):
    print('signal dispatched')