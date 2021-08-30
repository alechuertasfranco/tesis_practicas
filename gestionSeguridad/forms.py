from django import forms 
from django.forms import fields
from .models import Alumno, Docente


class AlumnoForm(forms.ModelForm):
    class Meta:
        model=Alumno
        fields='__all__'
        
class DocenteForm(forms.ModelForm):
    class Meta:
        model=Docente
        fields='__all__'
