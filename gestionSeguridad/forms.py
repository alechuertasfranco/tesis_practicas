from django import forms 
from django.forms import fields
from .models import Alumno, Docente, Facultad, Escuela

class AlumnoForm(forms.ModelForm):  
    class Meta:
        model=Alumno
        #fields='__all__'
        fields=['user','nro_matricula','apellidos','nombres','email','telefono','facultad','escuela','ciclo_academico'] 
    
class DocenteForm(forms.ModelForm):
    class Meta:
        model=Docente
        fields=['user','apellidos','nombres','titulo','telefono','email']
