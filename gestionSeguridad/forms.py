from django import forms 
from django.forms import fields
from .models import Alumno, Docente

class AlumnoForm(forms.ModelForm):  
    class Meta:
        model=Alumno
        #fields='__all__'
        fields=['nro_matricula','apellidos','nombres','email','telefono','facultad','escuela','ciclo_academico'] 
    
class DocenteForm(forms.ModelForm):
    class Meta:
        model=Docente
        fields=['apellidos','nombres','titulo','telefono','dni','email']

