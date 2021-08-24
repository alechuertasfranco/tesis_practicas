from django import forms 
from django.forms import fields
from .models import Alumno, Asesor,Jurado


class AlumnoForm(forms.ModelForm):
    class Meta:
        model=Alumno    
        fields='__all__'
        
class AsesorForm(forms.ModelForm):
    class Meta:
        model=Asesor   
        fields='__all__'
              
class JuradoForm(forms.ModelForm):
    class Meta:
        model=Jurado    
        fields='__all__'