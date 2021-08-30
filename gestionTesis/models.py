from gestionSeguridad.models import Alumno, Docente
from django.db import models

# Create your models here.
class PlanTesis(models.Model):
  fecha_presentacion = models.DateField()
  fecha_sustentacion = models.DateField()
  ultima_edicion = models.DateTimeField()
  documento = models.FileField(upload_to="plan_tesis", null=True)
  estado = models.BooleanField(default=True)
  alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
  asesor = models.ForeignKey(Docente, on_delete=models.CASCADE)
  def __str__(self):
      return self.nombres +" "+ self.apellidos