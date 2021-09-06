from gestionSeguridad.models import Alumno, Docente
from django.db import models

# Create your models here.
class PlanTesis(models.Model):
  fecha_presentacion = models.DateField()
  fecha_sustentacion = models.DateField(null=True)
  ultima_edicion = models.DateTimeField(null=True)
  proyecto_tesis = models.FileField(upload_to="plan_tesis", null=True)
  informe_final = models.FileField(upload_to="plan_tesis", null=True)
  estado = models.CharField(max_length=10, default="CREADO")
  alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
  asesor = models.ForeignKey(Docente, on_delete=models.CASCADE)
  def __str__(self):
      return self.alumno.apellidos
    
class JuradoTesis(models.Model):
  docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
  plan_tesis = models.ForeignKey(PlanTesis, on_delete=models.CASCADE)
  descripcion = models.CharField(max_length=500)
  documento = models.FileField(upload_to="plan_tesis_observado", null=True)
  estado = models.BooleanField(default=True)
  class Meta:
      unique_together = (("docente", "plan_tesis"),)