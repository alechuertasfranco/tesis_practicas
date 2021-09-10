from django.forms import *
from django.forms.widgets import HiddenInput
from .models import JuradoTesis, PlanTesis


class PlanTesisFormCreate(ModelForm):
    class Meta:
        model = PlanTesis
        fields = ['alumno', 'asesor', 'fecha_presentacion', 'proyecto_tesis', 'ultima_edicion']
        widgets = {
            'alumno': HiddenInput(),
            'ultima_edicion': HiddenInput(),
            'fecha_presentacion': TextInput(attrs={'type': 'date'}),
        }

class PlanTesisFormEdit(ModelForm):
    fecha_sustentacion = DateField(
        required=False,
        widget=TextInput(attrs={'type': 'date', 'readonly': 'true'})
    )
    informe_final = FileField(required=False)
    class Meta:
        model = PlanTesis
        fields = ['asesor', 'fecha_presentacion','fecha_sustentacion', 'proyecto_tesis', 'informe_final']
        widgets = {
            'asesor': Select(attrs={'readonly': 'true'}),
            'fecha_presentacion': TextInput(attrs={'type': 'date', 'readonly': 'true'}),
        }

class PlanTesisFormVisar(ModelForm):
    class Meta:
        model = PlanTesis
        fields = ['id', 'proyecto_tesis']

class JuradoTesisForm(ModelForm):
    class Meta:
        model = JuradoTesis
        fields = ['id', 'descripcion', 'documento', 'estado']
        widgets = {
            'estado': Select(choices=[('PENDIENTE','PENDIENTE'), ('APROBADO','APROBADO')]),
            'descripcion': Textarea(attrs={'rows':4}),
        }