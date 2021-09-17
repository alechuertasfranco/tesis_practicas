from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from django.shortcuts import redirect, render
from gestionSeguridad.models import *
from gestionTesis.models import *
from gestionTesis.forms import *
from gestionPracticas.models import PlanPracticas
from gestionSeguridad.views import group_required

import smtplib
import datetime
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
                _plan_tesis = PlanTesis.objects.get(alumno=_alumno.id)
                _hoy = datetime.date.today()

                if _hoy > (_plan_tesis.fecha_presentacion - datetime.timedelta(days=3)):
                    _correo_asunto = 'AVISO: Proyecto de Tesis - Presentación'
                    _correo_mensaje = 'Estimado {}\nEl tiempo restante para la presentación de su proyecto de tesis esta pronto a culminar, recuerde presentar su proyecto antes del {}'.format(_alumno.apellidos+", "+_alumno.nombres, _plan_tesis.fecha_presentacion)
                    enviar_correo(_correo_asunto, _correo_mensaje, _alumno.email)
                    
                if _plan_tesis.fecha_sustentacion:
                    if _hoy > (_plan_tesis.fecha_sustentacion - datetime.timedelta(days=3)):
                        _correo_asunto = 'AVISO: Proyecto de Tesis - Sustentación'
                        _correo_mensaje = 'Estimado {}\nEl tiempo restante para la sustentación de su proyecto de tesis esta pronto a culminar, recuerde que su sustentación esta programada para el día {}'.format(_alumno.apellidos+", "+_alumno.nombres, _plan_tesis.fecha_sustentacion)
                        enviar_correo(_correo_asunto, _correo_mensaje, _alumno.email)
                
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
    _data = {'alumno': _alumno, 'ultima_edicion': datetime.datetime.now()}
    _form = PlanTesisFormCreate(initial=_data)
    if request.method == "POST":
        _form = PlanTesisFormCreate(data=request.POST, files=request.FILES)
        if _form.is_valid():
            _form.save()
            _docente = Docente.objects.get(id = request.POST['asesor'])
            _correo_asunto = 'Asignación de asesoría de tesis'
            _correo_mensaje = 'Estimado {}\nHa sido asignado como asesor de proyecto de tesis para el alumno {}'.format(_docente.titulo + " " + _docente.apellidos, _alumno.apellidos+", "+_alumno.nombres)
            enviar_correo(_correo_asunto, _correo_mensaje, _docente.email)
            return redirect("index_estudiante")
    else:
        return {'form': _form }

def plan_tesis_edit(alumno_id, request):
    _plan_tesis = PlanTesis.objects.get(alumno=alumno_id)
    _form = PlanTesisFormEdit(instance=_plan_tesis)
    _form.ultima_edicion = _plan_tesis.ultima_edicion
    
    _observaciones = JuradoTesis.objects.filter(plan_tesis=_plan_tesis.id)
    if request.method == "POST":
        _plan_tesis.ultima_edicion = datetime.datetime.now()
        _form = PlanTesisFormEdit(data=request.POST, instance=_plan_tesis, files=request.FILES)
        if _form.is_valid():
            _form.save()
            return redirect("index_estudiante")
    else:
        return {'form': _form, 'observaciones': _observaciones}


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
        _plan_tesis.ultima_edicion = datetime.datetime.now()
        _plan_tesis.estado = "VISADO"
        _form = PlanTesisFormVisar(data=request.POST, instance=_plan_tesis, files=request.FILES)
        
        if _form.is_valid():
            asignar_jurados_aleatorios(_plan_tesis)
            _form.save()
        return redirect("index_docente")
    
    context = {'form': _form, 'plan_tesis': _plan_tesis}
    return render(request, "modal_visar.html", context)

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
        _alumno = Alumno.objects.get(id=_plan_tesis.alumno.id)
        _correo_asunto = 'Asignación de jurado de tesis'
        _correo_mensaje = 'Estimado {}\nHa sido asignado como jurado de proyecto de tesis para el alumno {}.'.format(_jurado.titulo + " " + _jurado.apellidos, _alumno.apellidos+", "+_alumno.nombres)
        enviar_correo(_correo_asunto, _correo_mensaje, _jurado.email)

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
        
        # Enviar correo de notificación de fecha de sustentación
        _alumno = Alumno.objects.get(id=_plan_tesis.alumno.id)
        _correo_asunto = 'AVISO: Programación de sustentación de tesis'
        _correo_mensaje = 'Estimado {}\nSu proyecto de tesis ha sido aprobado por los jurados y se le ha programado una fecha de sustentación para el día {}.'.format(_alumno.apellidos+", "+_alumno.nombres, _plan_tesis.fecha_sustentacion)
        enviar_correo(_correo_asunto, _correo_mensaje, _alumno.email)
    
    context = {'planes_tesis': _planes_tesis}
    return render(request, "index_secretaria.html", context)

# Vistas Auxiliares
def enviar_correo(asunto, mensaje, email):
    #MSG
    msg = MIMEMultipart()
    message = mensaje + '\n\nEste mensaje ha sido autogenerado por el equipo de sistemas.\nSi desea reportar un error, pongase en contacto con dirección de escuela'
    # setup the parameters of the message
    password = "5BGUr&OhNi"
    msg['From'] = "apracticastesis@gmail.com"
    msg['To'] = email
    msg['Subject'] = asunto
    msg["Date"] = formatdate(localtime=True)

    # add in the message body
    msg.attach(MIMEText(message, 'plain'))
    #create server
    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
    # Login Credentials for sending the mail
    server.login(msg['From'], password)
    # send the message via the server.
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()
    print ("successfully sent email to %s:" % (msg['To']))