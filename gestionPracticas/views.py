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
def agregarPractica(request):
    alumno=Alumno.objects.get(user=request.user.id)
    operacion=PlanPracticas.objects.filter(alumno=alumno).filter(estado= 'INCOMPLETO')
    if operacion:
        aux=str(int(operacion[0].id));
        id_operacion=aux.zfill(4)  
        fecha_dt = operacion[0].fecha_tramite.strftime('%Y-%m-%d')
        context={"alumno":alumno,'id_operacion':id_operacion,'fecha_operacion':fecha_dt,'modal': True} 
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
    return render(request,"practica/agregar/estudiante_practica.html",context)

def save_Practica(request):
    if request.method=="POST":
        _fecha_tramite=request.POST['fecha_tramite']
        _derecho_tramite=request.FILES['derecho_tramite']
        _plan_practicas=request.FILES['plan_practicas']
        _alumno=Alumno.objects.get(user=request.user.id)

        operacion=PlanPracticas.objects.filter(alumno=_alumno).filter(estado= 'INCOMPLETO')
        context={}
        if operacion:
            _plan_edit=PlanPracticas.objects.get(id = operacion[0].id)
            _plan_edit.derecho_tramite=_derecho_tramite
            _plan_edit.plan_practicas=_plan_practicas
            _plan_edit.save()
            _contacto=Contacto.objects.get(id = operacion[0].contacto.id)
            _empresa=Empresa.objects.get(id = operacion[0].empresa.id)
            if _contacto.nombres!= 'null' and _empresa.ruc != 'null':
                context={'contacto':_contacto,'empresa':_empresa}
        else:
            plan= PlanPracticas()
            plan.fecha_tramite=_fecha_tramite
            plan.derecho_tramite=_derecho_tramite
            plan.plan_practicas=_plan_practicas
            plan.alumno= _alumno
            plan.empresa= Empresa.objects.get(id = 1)
            plan.asesor= Docente.objects.get(id = 1)
            plan.contacto= Contacto.objects.get(id = 1)
            plan.estado="INCOMPLETO"
            plan.save()
            context={}
        return render(request,"practica/agregar/empresa_practica.html",context)
    return render(request,"practica/agregar/estudiante_practica.html")

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
        if operacion and operacion[0].empresa.id != 1:
            Empresa.objects.filter(id=operacion[0].empresa.id).update(razon_social=razon_social,ruc=ruc,direccion=direccion,ciudad=ciudad,gerente=gerente,telefono=telefono)
        else:
            empresa=Empresa()
            empresa.razon_social=razon_social
            empresa.ruc=ruc
            empresa.direccion=direccion
            empresa.ciudad=ciudad
            empresa.gerente=gerente
            empresa.telefono=telefono
            empresa.save()

        time.sleep(0.05)

        nombres=request.POST['nombres']
        cargo=request.POST['cargo']
        telefono=request.POST['telefono_C']
        email=request.POST['email']
        empresa=Empresa.objects.latest('id')
                
        if operacion and operacion[0].empresa.id != 1:
            Contacto.objects.filter(id=operacion[0].contacto.id).update(nombres=nombres,cargo=cargo,telefono=telefono,email=email,empresa=empresa)
        else:
            contacto= Contacto()
            contacto.nombres=request.POST['nombres']
            contacto.cargo=request.POST['cargo']
            contacto.telefono=request.POST['telefono_C']
            contacto.email=request.POST['email']
            contacto.empresa=Empresa.objects.latest('id')
            contacto.save()
            time.sleep(0.05)
            ultimo_registro=PlanPracticas.objects.latest('id')
            id=ultimo_registro.id
            PlanPracticas.objects.filter(id=id).update(empresa=Empresa.objects.latest('id'),contacto=Contacto.objects.latest('id'))

        docente=Docente.objects.filter(estado=True).distinct()
        context={'docente':docente}
        return render(request,"practica/agregar/asesor_practica.html",context)
    return render(request,"practica/agregar/empresa_practica.html")


def save_Asesor(request):
    if request.method=="POST":
        ultimo_registro=PlanPracticas.objects.latest('id')
        id=ultimo_registro.id
        docente=Docente.objects.get(id = request.POST['asesor_id'])
        PlanPracticas.objects.filter(id=id).update(asesor=docente, estado="Proceso")
        return redirect(reverse('listarPractica'))
    docente=Docente.objects.filter(estado=True).distinct()
    context={'docente':docente}
    return render(request,"practica/agregar/asesor_practica.html",context)
        
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


def listarPractica(request):
    alumno=Alumno.objects.get(user=request.user.id)
    plan_Incompleto=PlanPracticas.objects.filter(alumno=alumno).filter(estado= 'INCOMPLETO').distinct()
    planPractica=PlanPracticas.objects.filter(alumno=alumno).exclude(estado= 'INCOMPLETO').distinct()
    context={'planPractica': planPractica,'plan_Incompleto':plan_Incompleto}
    return render(request,"practica/index.html",context)


def listarPractica_aceptado(request):
    id='00145'
    descripcion="EMC SERVICIOS / SÁNCHEZ TICONA ROBERT JERRY/ Fecha_Presentacion:03/09/21"
    estado="Por Presentar"
    msg="si"
    context={'id':id,'descripcion':descripcion,'estado':estado,'msg':msg}
    return render(request,"practica/index2.html",context)   