from django.shortcuts import redirect, render
from datetime import datetime
from gestionSeguridad.models import *
from gestionTesis.models import *
from gestionTesis.forms import *
import logging
logger = logging.getLogger(__name__)

# Vistas para estudiantes
def index_estudiante(request):
    _alumno = Alumno.objects.get(user=request.user.id)
    _plan_tesis = PlanTesis.objects.filter(alumno=_alumno.id)
    
    logger.warning(_alumno.id)
    
    if _plan_tesis:
        _data = plan_tesis_edit(_alumno.id, request)
        _form = _data['form']
        observaciones = _data["observaciones"]
    else:
        _data = plan_tesis_create(_alumno.id, request)
        _form = _data['form']

    context = {'form': _form, 'plan_tesis': _plan_tesis, 'observaciones': observaciones}
    return render(request, "index_estudiante.html", context)


def plan_tesis_create(alumno_id, request):
    _alumno = Alumno.objects.get(id = alumno_id)
    _data = {'alumno': _alumno, 'ultima_edicion': datetime.now()}
    _form = PlanTesisFormCreate(initial=_data)
    if request.method == "POST":
        _form = PlanTesisFormCreate(_data=request.POST, files=request.FILES)
        if _form.is_valid():
            _form.save()
            return redirect("index_estudiante")
    else:
        return {'form': _form }

def plan_tesis_edit(alumno_id, request):
    _plan_tesis = PlanTesis.objects.get(alumno=alumno_id)
    _form = PlanTesisFormEdit(instance=_plan_tesis)
    _form.ultima_edicion = _plan_tesis.ultima_edicion
    
    _observaciones = JuradoTesis.objects.filter(plan_tesis=_plan_tesis.id)
    if request.method == "POST":
        _plan_tesis.ultima_edicion = datetime.now()
        _form = PlanTesisFormEdit(data=request.POST, instance=_plan_tesis, files=request.FILES)
        if _form.is_valid():
            _form.save()
            return redirect("index_estudiante")
    else:
        return {'form': _form, 'observaciones': _observaciones}


def index_estudiante_error(request):
    context = {'modal': True}
    return render(request, "index_estudiante.html", context)

# Vistas para jurado
def index_jurado(request):
    context = {}
    return render(request, "index_jurado.html", context)

def asignar_jurado(request):
    _form = JuradoTesisForm() 
    
    if request.method == "POST": 
        _form=JuradoTesisForm(request.POST)
        if _form.is_valid(): 
            _form.save() 
            return redirect("listardocente")
        
    context = {'form':_form}
    return render(request, "asignar_jurado.html", context)

# Vistas para secretaria
def index_secretaria(request):
    context = {}
    return render(request, "index_secretaria.html", context)
