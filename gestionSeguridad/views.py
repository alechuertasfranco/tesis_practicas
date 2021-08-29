from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from gestionSeguridad.models import Docente,Alumno
from django.core.paginator import Paginator
from .forms import AlumnoForm,DocenteForm
from django.http import Http404
from django.db.models import Q

# Create your views here.
def acceder(request):
    if request.method == 'POST':        
        form = AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            nombre_usuario = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            usuario = authenticate(username=nombre_usuario,password=password)
            if usuario is not None:
                login(request,usuario)
                return redirect("home")
            else:
                messages.error(request, "Los datos son incorrectos")
        else:
            messages.error(request,"Los datos son incorrectos")
    
    
    form = AuthenticationForm()
    return render(request,"login.html",{"form":form})

def homePage(request):    
    context = {}
    return render(request, "bienvenido.html", context)

def salir(request):
    logout(request)
    messages.info(request, "Saliste exitosamente")
    return redirect("login")

#Alumnos
@login_required(login_url="/")
def listaralumno(request):
    queryset=request.GET.get("buscar") 
    alumno=Alumno.objects.filter(estado=True) 
    page=request.GET.get("page", 1) 
    try: 
        paginator=Paginator(alumno,3) 
        alumno=paginator.page(page) 
    except: 
        raise Http404  
    if queryset:
        alumno=Alumno.objects.filter(
            Q(apellidos__icontains=queryset),estado=True
        ).distinct()
        context={'entity':alumno} 
    else:
        context={'entity':alumno, 'paginator':paginator} 
    return render(request,"alumnos/listar.html", context)

@login_required(login_url="/")
def agregaralumno(request): 
    form=AlumnoForm() 
    if request.method == "POST": 
        form=AlumnoForm(request.POST)
        if form.is_valid(): 
            form.estado=True
            form.save() 
            return redirect("listaralumno") 
    context={'form':form}
    return render(request, "alumnos/agregar.html", context)

@login_required(login_url="/")
def editaralumno(request,id):
    alumno=Alumno.objects.get(id=id) 
    if request.method=="POST": 
        form=AlumnoForm(request.POST,instance=alumno) 
        if form.is_valid(): 
            form.save() 
            return redirect("listaralumno") 
    else:
        form=AlumnoForm(instance=alumno)
    context={'form':form}
    return render(request,"alumnos/editar.html",context)

@login_required(login_url="/")
def eliminaralumno(request,id): 
    alumno=Alumno.objects.get(id=id) 
    alumno.estado=False 
    alumno.save()
    messages.error(request, "Eliminado correctamente")
    return redirect("listaralumno")

#Docentes
@login_required(login_url="/")
def listardocente(request):
    queryset=request.GET.get("buscar") 
    docente=Docente.objects.filter(estado=True) 
    page=request.GET.get("page", 1) 
    try: 
        paginator=Paginator(docente,3) 
        docente=paginator.page(page) 
    except: 
        raise Http404  
    if queryset:
        docente=Docente.objects.filter(
            Q(apellidos__icontains=queryset),estado=True
        ).distinct()
        context={'entity':docente} 
    else:
        context={'entity':docente, 'paginator':paginator} 
    return render(request,"docentes/listar.html", context)

@login_required(login_url="/")
def agregardocente(request): 
    form=DocenteForm() 
    if request.method == "POST": 
        form=DocenteForm(request.POST)
        if form.is_valid(): 
            form.save() 
            return redirect("listardocente") 
    context={'form':form}
    return render(request, "docentes/agregar.html", context)

@login_required(login_url="/")
def editardocente(request,id):
    docente=Docente.objects.get(id=id) 
    if request.method=="POST": 
        form=DocenteForm(request.POST,instance=docente) 
        if form.is_valid(): 
            form.save() 
            return redirect("listardocente") 
    else:
        form=DocenteForm(instance=docente)
    context={'form':form}
    return render(request,"docentes/editar.html",context)

@login_required(login_url="/")
def eliminardocente(request,id): 
    docente=Docente.objects.get(id=id) 
    docente.estado=False 
    docente.save()
    messages.error(request, "Eliminado correctamente")
    return redirect("listardocente")