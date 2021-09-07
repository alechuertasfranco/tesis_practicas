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
# Create your views here.
def agregarPractica(request):
    id=request.user.id
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
    alumno=Alumno.objects.raw('SELECT * FROM "gestionSeguridad_alumno" WHERE id=%s LIMIT 1',[id])[0]
    context={"alumno":alumno,'id_operacion':id_operacion}
    return render(request,"practica/agregar/estudiante_practica.html",context)

def save_Practica(request):
    if request.method=="POST":
        plan= PlanPracticas()
        plan.fecha_tramite=request.POST['fecha_tramite']
        plan.derecho_tramite=request.FILES['derecho_tramite']
        plan.plan_practicas=request.FILES['plan_practicas']
        plan.alumno= Alumno.objects.get(id = request.POST['alumno_id'])
        plan.empresa= Empresa.objects.get(id = 1 )
        plan.asesor= Docente.objects.get(id = 1)
        plan.contacto= Contacto.objects.get(id = 1)
        plan.estado="INCOMPLETO"
        plan.save()
        return render(request,"practica/agregar/empresa_practica.html")
    return render(request,"practica/agregar/estudiante_practica.html")

def save_Empresa(request):
    if request.method=="POST":
        empresa=Empresa()
        empresa.razon_social=request.POST['razon_social']
        empresa.ruc=request.POST['ruc']
        empresa.direccion=request.POST['direccion']
        empresa.ciudad=request.POST['ciudad']
        empresa.gerente=request.POST['gerente']
        empresa.telefono=request.POST['telefono_E']
        empresa.save()

        time.sleep(0.05)
        
        contacto= Contacto()
        contacto.apellidos="HOla"
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
    
    id_alumno=request.user.id
    alum=Alumno.objects.get(id = id_alumno)
    planPractica=PlanPracticas.objects.filter(alumno=alum).exclude(estado= 'INCOMPLETO').distinct()
    context={'planPractica': planPractica}
    return render(request,"practica/index.html",context)

def listarPractica_id(request):
    id='00145'
    descripcion="EMC SERVICIOS / SÁNCHEZ TICONA ROBERT JERRY"
    estado="Proceso"
    context={'id':id,'descripcion':descripcion,'estado':estado}
    return render(request,"practica/index.html",context)

def listarPractica_aceptado(request):
    id='00145'
    descripcion="EMC SERVICIOS / SÁNCHEZ TICONA ROBERT JERRY/ Fecha_Presentacion:03/09/21"
    estado="Por Presentar"
    msg="si"
    context={'id':id,'descripcion':descripcion,'estado':estado,'msg':msg}
    return render(request,"practica/index2.html",context)   