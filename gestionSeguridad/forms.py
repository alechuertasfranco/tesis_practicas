from django import forms 
from django.forms import fields
from .models import Alumno, Docente


class AlumnoForm(forms.ModelForm):
    class Meta:
        model=Alumno    
        fields=['nombre','apellidos','email','dni'] 
        
class DocenteForm(forms.ModelForm):
    class Meta:
        model=Docente   
        fields=['nombre','apellidos','email','dni'] 
