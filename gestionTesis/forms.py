from django import forms
from django.forms import TextInput
from .models import PlanTesis


class PlanTesisForm(forms.ModelForm):
    class Meta:
        model=PlanTesis
        fields=['asesor','fecha_presentacion','fecha_sustentacion','documento']
        widgets = {
            'fecha_presentacion': TextInput(attrs={'type': 'date','readonly':'true'}),
            'fecha_sustentacion': TextInput(attrs={'type': 'date','readonly':'true'}),
        }