from django.shortcuts import render
from gestionSeguridad.models import Alumno,Docente
# Create your views here.
def agregarPractica(request,id):
    alumno=Alumno.objects.raw('SELECT * FROM "gestionSeguridad_alumno" WHERE id=%s LIMIT 1',[id])[0]
    context={"alumno":alumno}
    return render(request,"practica/agregar/estudiante_practica.html",context)

def save_Practida(request):
    return render(request,"practica/agregar/empresa_practica.html")

def save_Empresa(request):
    return render(request,"practica/agregar/asesor_practica.html")

def save_Asesor(request):

    render(request,"practica/index.html")
        

def listarPractica(request):
    msg="no"
    id=request.user.id
    context={'msg':msg,'id':id}
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