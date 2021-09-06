from django.contrib import admin
from gestionSeguridad.models import Alumno,Docente
from gestionPracticas.models import Empresa,Contacto,PlanPracticas
# Register your models here.

admin.site.register(Alumno)
admin.site.register(Empresa)
admin.site.register(Contacto)
admin.site.register(Docente)
admin.site.register(PlanPracticas)