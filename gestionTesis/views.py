from django.shortcuts import redirect, render
from datetime import datetime
from gestionSeguridad.models import *
from gestionTesis.models import *
from gestionPracticas.models import PlanPracticas
from gestionTesis.forms import *
from gestionSeguridad.views import group_required

import logging
import random
logger = logging.getLogger(__name__)

# Vistas para estudiantes
@group_required('Alumno')
def index_estudiante(request):
    _alumno = Alumno.objects.get(user=request.user.id)
    _planes_practicas = PlanPracticas.objects.filter(alumno=_alumno.id)
    _plan_tesis = PlanTesis.objects.filter(alumno=_alumno.id)
    context = {'modal': True}
    
    if _planes_practicas:
        _plan_practicas = PlanPracticas.objects.get(alumno=_alumno.id)
        if _plan_practicas.resolucion:
            
            _observaciones = []
            _form = []
            
            if _plan_tesis:
                _data = plan_tesis_edit(_alumno.id, request)
                if type(_data) is dict:
                    _form = _data['form']
                    _observaciones = _data['observaciones']
                else:
                    return _data
            else:
                _data = plan_tesis_create(_alumno.id, request)
                if type(_data) is dict:
                    _form = _data['form']
                else:
                    return _data
            
            context = {'form': _form, 'plan_tesis': _plan_tesis, 'observaciones': _observaciones}
        
        else:
            logger.warning("No hay resolucion")
    else:
        logger.warning("No hay plan")
    
    return render(request, "index_estudiante.html", context)


def plan_tesis_create(alumno_id, request):
    _alumno = Alumno.objects.get(id = alumno_id)
    _data = {'alumno': _alumno, 'ultima_edicion': datetime.now()}
    _form = PlanTesisFormCreate(initial=_data)
    if request.method == "POST":
        _form = PlanTesisFormCreate(data=request.POST, files=request.FILES)
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

@group_required('Alumno')
def index_estudiante_error(request):
    context = {'modal': True}
    return render(request, "index_estudiante.html", context)

# Vistas para jurado
@group_required('Docente')
def index_docente(request):
    _docente = Docente.objects.get(user=request.user.id)
    _asesorados = PlanTesis.objects.filter(asesor = _docente.id)
    _evaluados = JuradoTesis.objects.filter(docente = _docente.id)
    if request.method == "POST":
        logger.warning("INDEX_DOCENTE")  
    
    context = {'docente': _docente, 'asesorados': _asesorados, 'evaluados':_evaluados}
    return render(request, "index_docente.html", context)

@group_required('Docente')
def visar_plan_tesis(request, plan_id):
    _plan_tesis = PlanTesis.objects.get(id=plan_id)
    _form = PlanTesisFormVisar(instance=_plan_tesis)
    
    if request.method == "POST":
        _plan_tesis.ultima_edicion = datetime.now()
        _plan_tesis.estado = "VISADO"
        _form = PlanTesisFormVisar(data=request.POST, instance=_plan_tesis, files=request.FILES)
        
        if _form.is_valid():
            asignar_jurados_aleatorios(_plan_tesis)
            _form.save()
        return redirect("index_docente")
    
    context = {'form': _form, 'plan_tesis': _plan_tesis}
    return render(request, "modal_visar.html", context)

@group_required('Docente')
def asignar_jurados_aleatorios(_plan_tesis):
    _pool= list(Docente.objects.all())
    random.shuffle(_pool)
    _jurados = _pool[:100]
    logger.warning(_jurados)
    
    for _jurado in _jurados:
        _observacion = JuradoTesis(
            docente = _jurado,
            plan_tesis = _plan_tesis,
        )
        _observacion.save()

@group_required('Docente')
def observar_plan_tesis(request, observacion_id):
    _observacion = JuradoTesis.objects.get(id=observacion_id)
    _form = JuradoTesisForm(instance=_observacion)
    
    if request.method == "POST":
        # Registrar Observación
        _form = JuradoTesisForm(data=request.POST, instance=_observacion, files=request.FILES)
        if _form.is_valid():
            logger.warning("IS VALID")
            _form.save()
            
            # Cambiar el estado del Plan si tiene todo aprobado
            if request.POST['estado'] == 'APROBADO':
                _plan_tesis = PlanTesis.objects.get(id=_observacion.plan_tesis.id)
                _estado_previo = _plan_tesis.estado
                _plan_tesis.estado='APROBADO'
                _observaciones = JuradoTesis.objects.filter(plan_tesis=_plan_tesis.id)
                for item in _observaciones:
                    if item.estado != 'APROBADO':
                        _plan_tesis.estado = _estado_previo
                _plan_tesis.save()
                logger.warning(_plan_tesis.estado)
            
        return redirect("index_docente")
    
    context = {'form': _form, 'observacion': _observacion}
    return render(request, "modal_observar.html", context)

# Vistas para secretaria
@group_required('Secretaria')
def index_secretaria(request):
    _planes_tesis = PlanTesis.objects.filter(fecha_sustentacion=None);
    
    if request.method == "POST":
        _plan_tesis = PlanTesis.objects.get(id=request.POST['id'])
        _plan_tesis.fecha_sustentacion = request.POST['fecha_sustentacion']
        _plan_tesis.save()
    
    context = {'planes_tesis': _planes_tesis}
    return render(request, "index_secretaria.html", context)
