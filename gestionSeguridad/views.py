from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from gestionSeguridad.models import Docente, Alumno, Escuela, Facultad
from django.core.paginator import Paginator
from .forms import AlumnoForm, DocenteForm
from django.http import Http404
from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test
#EMAIL
# import necessary packages
 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

def group_required(*group_names):
    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups, login_url='home')

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
                messages.success(request, "Ingresó correctamente")
                return redirect("home")            
            else:
                messages.error(request, "Los datos son incorrectos")
        else:
            messages.error(request,"Los datos son incorrectos")
    form = AuthenticationForm()
    return render(request,"login.html",{"form":form})

@login_required(login_url="/")
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
    if request.user.is_staff:
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
    else:
        return redirect('home')

@login_required(login_url="/")
def agregaralumno(request):
    form=AlumnoForm() 
    if request.user.is_staff:
        if request.method == "POST": 
            form=AlumnoForm(request.POST)
            if form.is_valid(): 
                alumno = form.save(commit=False)
                cadena = alumno.email
                indice = cadena.index('@')
                #MSG
                msg = MIMEMultipart()
                message = "El usuario de su cuenta es: "+ cadena[:indice] + " y la contraseña es: " + alumno.nro_matricula
                # setup the parameters of the message
                password = "5BGUr&OhNi"
                msg['From'] = "apracticastesis@gmail.com"
                msg['To'] = alumno.email
                msg['Subject'] = "Cuenta de usuario"

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
                
                user = User.objects.create_user(username = cadena[:indice], 
                                                first_name = alumno.nombres,
                                                last_name = alumno.apellidos,
                                                email=alumno.email, 
                                                password=alumno.nro_matricula)
                group = Group.objects.get(name='GrupoAlumno')
                user.groups.add(group)
                user.save()
                alumno.user = user
                alumno.estado = True
                alumno.save()
                messages.success(request, "Se agregó correctamente")
                return redirect("listaralumno") 
        context={'form':form}
        return render(request, "alumnos/agregar.html", context)
    return redirect("home")

@login_required(login_url="/")
def editaralumno(request,id):
    if request.user.is_staff:
        alumno=Alumno.objects.get(id=id) 
        if request.method=="POST": 
            form=AlumnoForm(request.POST,instance=alumno) 
            if form.is_valid(): 
                form.save() 
                return redirect("listaralumno") 
        else:
            form=AlumnoForm(instance=alumno)
        context={'form':form}
        messages.info(request, "Se editó correctamente")
        return render(request,"alumnos/editar.html",context)
    return redirect("home")

@login_required(login_url="/")
def eliminaralumno(request,id): 
    if request.user.is_staff:
        alumno=Alumno.objects.get(id=id)        
        user = alumno.user
        user.is_active = False
        user.save()
        alumno.estado=False 
        alumno.save()
        messages.error(request, "Eliminado correctamente")
        return redirect("listaralumno")
    return redirect("home")

@login_required(login_url="/")
def load_escuelas(request):
    facultad_id = request.GET.get('facultad_id')
    escuelas = Escuela.objects.filter(facultad_id=facultad_id).order_by('descripcion')
    return render(request, 'alumnos/escuelas.html', {'escuelas': escuelas})

#Docentes
@login_required(login_url="/")
def listardocente(request):
    if request.user.is_staff:
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
    return redirect("home")

@login_required(login_url="/")
def agregardocente(request): 
    form=DocenteForm() 
    if request.user.is_staff:
        if request.method == "POST": 
            form=DocenteForm(request.POST)
            if form.is_valid(): 
                docente = form.save(commit=False)
                cadena = docente.email
                indice = cadena.index('@')
                #MSG
                msg = MIMEMultipart()
                message = "El usuario de su cuenta es: "+ cadena[:indice] + " y la contraseña es: " + docente.dni
                # setup the parameters of the message
                password = "5BGUr&OhNi"
                msg['From'] = "apracticastesis@gmail.com"
                msg['To'] = docente.email
                msg['Subject'] = "Cuenta de usuario"
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
                user = User.objects.create_user(username = cadena[:indice], 
                                                first_name = docente.nombres,
                                                last_name = docente.apellidos,
                                                email=docente.email, 
                                                password=docente.dni)
                group = Group.objects.get(name='GrupoDocente')
                user.groups.add(group)
                user.save()
                docente.user = user
                docente.estado = True
                docente.save()            
                form.save() 
                messages.success(request, "Se agregó correctamente")                
                return redirect("listardocente") 
        context={'form':form}
        return render(request, "docentes/agregar.html", context)
    return redirect("home")

@login_required(login_url="/")
def editardocente(request,id):
    if request.user.is_staff:
        docente=Docente.objects.get(id=id) 
        if request.method=="POST": 
            form=DocenteForm(request.POST,instance=docente) 
            if form.is_valid(): 
                form.save() 
                return redirect("listardocente") 
        else:
            form=DocenteForm(instance=docente)
        context={'form':form}        
        messages.info(request, "Se editó correctamente")
        return render(request,"docentes/editar.html",context)
    return redirect("home")

@login_required(login_url="/")
def eliminardocente(request,id): 
    if request.user.is_staff:
        docente=Docente.objects.get(id=id) 
        user = docente.user
        user.delete()
        docente.estado=False 
        docente.save()
        messages.error(request, "Eliminado correctamente")
        return redirect("listardocente")
    return redirect("home")

