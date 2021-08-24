from django.shortcuts import render

# Create your views here.
def agregarPractica(request):
    return render(request,"practica/agregar/estudiante_practica.html")

def agregarEmpresa(request):
    return render(request,"practica/agregar/empresa_practica.html")

def agregarAsesor(request):
    return render(request,"practica/agregar/asesor_practica.html")

def listarPractica(request):
    msg="no"
    context={'msg':msg}
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