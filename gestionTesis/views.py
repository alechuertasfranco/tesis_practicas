from django.shortcuts import render

# Vistas para estudiantes
def index_estudiante(request):
  context={} 
  return render(request, "index_estudiante.html", context)
def index_estudiante_error(request):
  context={'modal': True} 
  return render(request, "index_estudiante.html", context)

# Vistas para jurado
def index_jurado(request):
  context={} 
  return render(request, "index_jurado.html", context)

# Vistas para secretaria
def index_secretaria(request):
  context={} 
  return render(request, "index_secretaria.html", context)