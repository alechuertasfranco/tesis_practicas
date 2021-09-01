from django.forms import *
from django.forms.widgets import HiddenInput
from .models import PlanTesis


class PlanTesisFormCreate(ModelForm):
    class Meta:
        model=PlanTesis
        fields=[ 'alumno','asesor','fecha_presentacion','proyecto_tesis']
        widgets = {
            'alumno': HiddenInput(),
            'fecha_presentacion': TextInput(attrs={'type': 'date'}),
        }
        
class PlanTesisFormEdit(ModelForm):
    class Meta:
        model=PlanTesis
        fields=['asesor','fecha_presentacion','fecha_sustentacion','proyecto_tesis', 'informe_final']
        widgets = {
            'asesor': Select(attrs={'disabled':'true'}),
            'fecha_presentacion': TextInput(attrs={'type': 'date','readonly':'true'}),
            'fecha_sustentacion': TextInput(attrs={'type': 'date','readonly':'true'}),
        }