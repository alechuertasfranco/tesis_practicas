import json
from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import render
from gestionSeguridad.models import Alumno,Docente
from gestionPracticas.models import Contacto, Empresa, PlanPracticas
from django.db.models import Q
from django.urls import reverse
from django.shortcuts import redirect

import time
from django.db import models
# Create your views here.

#Views para el estudiante
def listarPractica(request):
    alumno=Alumno.objects.get(user=request.user.id)
    plan_Incompleto=PlanPracticas.objects.filter(alumno=alumno).filter(estado= 'INCOMPLETO').distinct()
    planPractica=PlanPracticas.objects.filter(alumno=alumno).exclude(estado= 'INCOMPLETO').distinct()
    context={'planPractica': planPractica,'plan_Incompleto':plan_Incompleto}
    return render(request,"estudiante/index.html",context)

def agregarPractica(request):
    alumno=Alumno.objects.get(user=request.user.id)
    operacion=PlanPracticas.objects.filter(alumno=alumno).filter(estado= 'INCOMPLETO')
    if operacion:
        aux=str(int(operacion[0].id));
        id_operacion=aux.zfill(4)
        doc_derecho=str(operacion[0].derecho_tramite)[14:]
        doc_plan=str(operacion[0].plan_practicas)[14:]
        fecha_dt = operacion[0].fecha_tramite.strftime('%Y-%m-%d')
        context={"alumno":alumno,'id_operacion':id_operacion,'fecha_operacion':fecha_dt,'modal': True,'doc_derecho':doc_derecho,'doc_plan':doc_plan} 
    else:    
        try:
            id_operacion=PlanPracticas.objects.latest('id')
        except Exception as e:
            id_operacion=0
        aux=""
        if(id_operacion==0):
            id_operacion=1
            aux=str(id_operacion)
        else:
            aux=str(int(id_operacion.id)+1);
        id_operacion=aux.zfill(4)    
        alumno=Alumno.objects.get(user=request.user.id)
        context={"alumno":alumno,'id_operacion':id_operacion}
    return render(request,"estudiante/agregar/estudiante_practica.html",context)

def save_Practica(request):
    if request.method=="POST":
        _fecha_tramite=request.POST['fecha_tramite']
        _derecho_tramite=0
        _derecho_tramite=0
        try:
            _derecho_tramite=request.FILES['derecho_tramite']
            _plan_practicas=request.FILES['plan_practicas']
        except:
            print('no hay nada')
        
        _alumno=Alumno.objects.get(user=request.user.id)

        operacion=PlanPracticas.objects.filter(alumno=_alumno).filter(estado= 'INCOMPLETO')
        context={}
        if operacion:
            if _derecho_tramite!=0 and _plan_practicas!=0:
                _plan_edit=PlanPracticas.objects.get(id = operacion[0].id)
                _plan_edit.derecho_tramite=_derecho_tramite
                _plan_edit.plan_practicas=_plan_practicas
                _plan_edit.save()

            _plan_edit=PlanPracticas.objects.get(id = operacion[0].id)
            _plan_edit.fecha_tramite=_fecha_tramite
            _plan_edit.save()

            _contacto=Contacto.objects.get(id = operacion[0].contacto.id)
            _empresa=Empresa.objects.get(id = operacion[0].empresa.id)
            if _contacto.nombres!= 'null' and _empresa.ruc != 'null':
                context={'contacto':_contacto,'empresa':_empresa}
        else:
            Insert_Plan(_fecha_tramite,_derecho_tramite,_plan_practicas,_alumno)
            context={}
        return render(request,"estudiante/agregar/empresa_practica.html",context)
    return render(request,"estudiante/agregar/estudiante_practica.html")

def save_Empresa(request):
    if request.method=="POST":
        razon_social=request.POST['razon_social']
        ruc=request.POST['ruc']
        direccion=request.POST['direccion']
        ciudad=request.POST['ciudad']
        gerente=request.POST['gerente']
        telefono=request.POST['telefono_E']

        _alumno=Alumno.objects.get(user=request.user.id)
        operacion=PlanPracticas.objects.filter(alumno=_alumno).filter(estado= 'INCOMPLETO')
        context={}
        if operacion and operacion[0].empresa.id != 0:
            Empresa.objects.filter(id=operacion[0].empresa.id).update(razon_social=razon_social,ruc=ruc,direccion=direccion,ciudad=ciudad,gerente=gerente,telefono=telefono)
        else:
            Insert_Empresa(razon_social,ruc,direccion,ciudad,gerente,telefono)    
        time.sleep(0.05)

        nombres=request.POST['nombres']
        cargo=request.POST['cargo']
        telefono=request.POST['telefono_C']
        email=request.POST['email']
        empresa=Empresa.objects.latest('id')
                
        if operacion and operacion[0].empresa.id != 0:
            Contacto.objects.filter(id=operacion[0].contacto.id).update(nombres=nombres,cargo=cargo,telefono=telefono,email=email,empresa=empresa)
        else:
            Insert_Contacto(nombres,cargo,telefono,email,empresa)
            time.sleep(0.05)
            ultimo_registro=PlanPracticas.objects.latest('id')
            id=ultimo_registro.id
            PlanPracticas.objects.filter(id=id).update(empresa=Empresa.objects.latest('id'),contacto=Contacto.objects.latest('id'))

        docente=Docente.objects.filter(estado=True).distinct()
        context={'docente':docente}
        return render(request,"estudiante/agregar/asesor_practica.html",context)
    return render(request,"estudiante/agregar/empresa_practica.html")

def save_Asesor(request):
    if request.method=="POST":
        ultimo_registro=PlanPracticas.objects.latest('id')
        id=ultimo_registro.id
        docente=Docente.objects.get(id = request.POST['asesor_id'])
        PlanPracticas.objects.filter(id=id).update(asesor=docente, estado="PorVisar")
        return redirect(reverse('listarPractica'))
    docente=Docente.objects.filter(estado=True).distinct()
    context={'docente':docente}
    return render(request,"estudiante/agregar/asesor_practica.html",context)
        
def verAsesor(request,id):
    asesor=Docente.objects.get(id =id)
    data_asesor={}
    data_asesor['id']=asesor.id
    data_asesor['apellidos']=asesor.apellidos
    data_asesor['nombres']=asesor.nombres
    data_asesor['titulo']=asesor.titulo
    data_asesor['telefono']=asesor.telefono
    data_asesor['email']=asesor.email
    data = json.dumps(data_asesor)
    return HttpResponse(data,'application/json')

def Insert_Empresa(razon_social,ruc,direccion,ciudad,gerente,telefono):
    empresa=Empresa()
    empresa.razon_social=razon_social
    empresa.ruc=ruc
    empresa.direccion=direccion
    empresa.ciudad=ciudad
    empresa.gerente=gerente
    empresa.telefono=telefono
    empresa.save()

def Insert_Plan(fecha_tramite,derecho_tramite,plan_practicas,alumno):
    plan= PlanPracticas()
    plan.fecha_tramite=fecha_tramite
    plan.derecho_tramite=derecho_tramite
    plan.plan_practicas=plan_practicas
    plan.alumno= alumno
    plan.empresa= Empresa.objects.get(id = 0)
    plan.asesor= Docente.objects.get(id = 1)
    plan.contacto= Contacto.objects.get(id = 0)
    plan.estado="INCOMPLETO"
    plan.save()

def Insert_Contacto(nombres,cargo,telefono,email,empresa):
    contacto= Contacto()
    contacto.nombres=nombres
    contacto.cargo=cargo
    contacto.telefono=telefono
    contacto.email=email
    contacto.empresa=empresa
    contacto.save()

#Views para el asesor

def asesor_practica(request):
    _usario_id=request.user.id
    asesor=Docente.objects.get(user=_usario_id)
    plan=PlanPracticas.objects.filter(asesor=asesor)
    context={'planPractica':plan}
    return render(request,"asesor/index.html",context)

def fetchAlumnoPractica(request,id):
    alumno=Alumno.objects.get(id = id)
    plan=PlanPracticas.objects.get(alumno =alumno)
    data_alumno={}
    data_alumno['id_alumno']=alumno.id
    data_alumno['apellidos']=alumno.apellidos
    data_alumno['nombres']=alumno.nombres
    data_alumno['id_plan']=plan.id
    data = json.dumps(data_alumno)
    return HttpResponse(data,'application/json')

def save_Visado(request):
    if request.method=="POST":
        _plan=PlanPracticas.objects.get(id=request.POST['plan_id'])
        _plan.plan_practicas=request.FILES['plan_practicas']
        _plan.estado="Visado"
        _plan.save()
        return redirect(reverse('asesor_practica'))
    return redirect(reverse('asesor_practica'))

#Views para la secretaria

def secretaria_practica(request):
    plan=PlanPracticas.objects.filter(estado="Visado")
    context={'planPractica':plan}
    return render(request,"secretaria/index.html",context)

def perfil_alumno(request,id):
    plan=PlanPracticas.objects.filter(estado="Visado")
    context={'planPractica':plan}
    return render(request,"secretaria/perfil.html",context)

def save_fechaPresentacion(request):
    if request.method=="POST":
        _plan=PlanPracticas.objects.get(id=request.POST['plan_id'])
        _plan.plan_practicas=request.FILES['plan_practicas']
        _plan.estado="Visado"
        _plan.save()
        return redirect(reverse('asesor_practica'))
    return redirect(reverse('asesor_practica'))