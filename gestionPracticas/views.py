from django.shortcuts import render

# Create your views here.
def agregarPractica(request):
    return render(request,"practica/agregar/estudiante_practica.html")

def agregarEmpresa(request):
    return render(request,"practica/agregar/empresa_practica.html")

def agregarAsesor(request):
    return render(request,"practica/agregar/asesor_practica.html")

def listarPractica(request):
    return render(request,"practica/index.html")

def listarPractica_id(request):
    id='00145'
    descripcion="EMC SERVICIOS-SÁNCHEZ TICONA-PRACTICA"
    context={'id':id,'descripcion':descripcion}
    return render(request,"practica/index.html",context)   