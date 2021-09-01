from django.shortcuts import redirect, render
from gestionSeguridad.models import *
from gestionTesis.models import *
from gestionTesis.forms import *
import logging

# Vistas para estudiantes
def index_estudiante(request):
  logger = logging.getLogger(__name__)
  alumno = Alumno.objects.get(user=request.user.id)
  plan_tesis = PlanTesis.objects.filter(alumno=alumno.id)
  logger.warn(plan_tesis)
  if plan_tesis:
    plan_tesis = PlanTesis.objects.get(alumno=alumno.id)
    form=PlanTesisFormEdit(instance=plan_tesis)
    if request.method == "POST": 
      form=PlanTesisFormEdit(data=request.POST,instance=plan_tesis,files=request.FILES)
      if form.is_valid(): 
          form.save() 
          form.alumno=alumno.id
          return redirect("index_estudiante") 
  else:
    data = {'alumno': alumno}
    form=PlanTesisFormCreate(initial=data)
    if request.method == "POST": 
      form=PlanTesisFormCreate(data=request.POST,files=request.FILES)
      if form.is_valid(): 
          form.save()
          return redirect("index_estudiante") 
  context={'form': form, 'plan_tesis': plan_tesis}
  return render(request, "index_estudiante.html", context)

def index_estudiante_error(request):
  context={'modal': True} 
  return render(request, "index_estudiante.html", context)

# Vistas para jurado
def index_jurado(request):
  context={} 
  return render(request, "index_jurado.html", context)

# Vistas para secretaria
def index_secretaria(request):
  context={} 
  return render(request, "index_secretaria.html", context)