from typing import List
from django.http.request import QueryDict
from django.shortcuts import redirect, render, HttpResponse
from django.http import HttpResponse

# Modelos ---------------------------------------------------------------------------------
from AppCoder.models import Curso, Profesor

# Formularios -----------------------------------------------------------------------------
from AppCoder.forms import CursoFormulario, ProfesorFormulario, UserRegisterForm

# INICIO Vistas basadas en Clases ----------------------------------------------------------
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
# FIN Vistas basadas en clases --------------------------------------------------------------

# Importamos todo lo necesario para hacer autenticación ------------------------------------- 
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
# Fin Autenticación -------------------------------------------------------------------------

# Create your views here.

def curso(request):

      curso =  Curso(nombre="Desarrollo web", camada="19881")
      curso.save()
      documentoDeTexto = f"--->Curso: {curso.nombre}   Camada: {curso.camada}"


      return HttpResponse(documentoDeTexto)

#@login_required
def inicio(request):

      return render(request, "AppCoder/inicio.html")



def estudiantes(request):

      return render(request, "AppCoder/estudiantes.html")


def entregables(request):

      return render(request, "AppCoder/entregables.html")

@login_required
def cursos(request):

      if request.method == 'POST':

            miFormulario = CursoFormulario(request.POST) #aquí mellega toda la información del html

            print(miFormulario)

            if miFormulario.is_valid:   #Si pasó la validación de Django

                  informacion = miFormulario.cleaned_data

                  curso = Curso (nombre=informacion['curso'], camada=informacion['camada']) 

                  curso.save()

                  return render(request, "AppCoder/inicio.html") #Vuelvo al inicio o a donde quieran

      else: 

            miFormulario= CursoFormulario() #Formulario vacio para construir el html

      return render(request, "AppCoder/cursos.html", {"miFormulario":miFormulario})




def profesores(request):

      if request.method == 'POST':

            miFormulario = ProfesorFormulario(request.POST) #aquí mellega toda la información del html

            print(miFormulario)

            if miFormulario.is_valid:   #Si pasó la validación de Django

                  informacion = miFormulario.cleaned_data

                  profesor = Profesor (nombre=informacion['nombre'], apellido=informacion['apellido'],
                   email=informacion['email'], profesion=informacion['profesion']) 

                  profesor.save()

                  return render(request, "AppCoder/inicio.html") #Vuelvo al inicio o a donde quieran

      else: 

            miFormulario= ProfesorFormulario() #Formulario vacio para construir el html

      return render(request, "AppCoder/profesores.html", {"miFormulario":miFormulario})






def buscar(request):

      if  request.GET["camada"]:

	      #respuesta = f"Estoy buscando la camada nro: {request.GET['camada'] }" 
            camada = request.GET['camada'] 
            cursos = Curso.objects.filter(camada__icontains=camada)

            return render(request, "AppCoder/inicio.html", {"cursos":cursos, "camada":camada})

      else: 

	      respuesta = "No enviaste datos"
      return HttpResponse(respuesta)
      #No olvidar from django.http import HttpResponse


def leerProfesores(request):

      profesores = Profesor.objects.all() #trae todos los profesores

      contexto= {"profesores":profesores} 

      return render(request, "AppCoder/leerProfesores.html",contexto)



def eliminarProfesor(request, profesor_nombre):

      profesor = Profesor.objects.get(nombre=profesor_nombre)
      profesor.delete()
      
      #vuelvo al menú
      profesores = Profesor.objects.all() #trae todos los profesores

      contexto= {"profesores":profesores} 

      return render(request, "AppCoder/leerProfesores.html",contexto)



def editarProfesor(request, profesor_nombre):

      #Recibe el nombre del profesor que vamos a modificar
      profesor = Profesor.objects.get(nombre=profesor_nombre)

      #Si es metodo POST hago lo mismo que el agregar
      if request.method == 'POST':

            miFormulario = ProfesorFormulario(request.POST) #aquí mellega toda la información del html

            print(miFormulario)

            if miFormulario.is_valid:   #Si pasó la validación de Django

                  informacion = miFormulario.cleaned_data

                  profesor.nombre = informacion['nombre']
                  profesor.apellido = informacion['apellido']
                  profesor.email = informacion['email']
                  profesor.profesion = informacion['profesion']

                  profesor.save()

                  return render(request, "AppCoder/inicio.html") #Vuelvo al inicio o a donde quieran
      #En caso que no sea post
      else: 
            #Creo el formulario con los datos que voy a modificar
            miFormulario= ProfesorFormulario(initial={'nombre': profesor.nombre, 'apellido':profesor.apellido , 
            'email':profesor.email, 'profesion':profesor.profesion}) 

      #Voy al html que me permite editar
      return render(request, "AppCoder/editarProfesor.html", {"miFormulario":miFormulario, "profesor_nombre":profesor_nombre})




class CursoList(LoginRequiredMixin,ListView):

      model = Curso 
      template_name = "AppCoder/cursos_list.html"



class CursoDetalle(LoginRequiredMixin,DetailView):

      model = Curso
      template_name = "AppCoder/curso_detalle.html"


#
class CursoCreacion(LoginRequiredMixin,CreateView):

      model = Curso
      success_url = "/AppCoder/curso/list"
      fields = ['nombre', 'camada']


class CursoUpdate(UpdateView):

      model = Curso
      success_url = "/AppCoder/curso/list"
      fields  = ['nombre', 'camada']


class CursoDelete(DeleteView):

      model = Curso
      success_url = "/AppCoder/curso/list"
     

#iniciamos el login
def login_request(request):
      #capturamos el post - Es decir verificamos que el metodo por el cual viene la solicitud
      # Se trate del meotodo "POST" y no del metodo "GET"
      # POR QUE EN EL METODO POST 
      """
      Caché y registro del servidor	
      GET : Los parámetros URL se guardan sin cifrar.	
      """
      
      if request.method == "POST":
            #inicio esl uso del formulario de autenticación que me da Django
            #me toma dos parámetros el request y los datos que toma del request
            # El AuthenticationForm lo provee la aplicación de autenticación incorporada en Django
            # Si vamos a setting.py del proyecto podremos ver la aplicaciones ya incorporadas en 
            # Django
            # Se le pasa como argumento el request o solicitud o peticion HTTP
            form = AuthenticationForm(request, data = request.POST)
            
            # Tenemos una validación del formulario mediante el metodo is_valid()
            # Por ejemplo debe saber si tiene la validación del token 
            if form.is_valid():
                  # En el caso de que el formulario no tiene errores, es decir si es valido
                  # Se crean dos variables y se extraen los datos necesarios para utenticar 
                  # cleaned_data nos permite limpiar la información que viene en los dos campos
                  usuario = form.cleaned_data.get('username')
                  contra = form.cleaned_data.get('password')
               
                  # En este punto con la función "authenticate"
                  # Determina si las credenciales son validas,  
                  # en el caso de ser validas retorna un objeto user 
                  user = authenticate(username = usuario , password = contra)
                 
                  if user is not None:
                        
                        """
                        Conservar una identificación de usuario y un backend en la solicitud.
                        De esta manera, un usuario no tiene que volver a autenticarse en 
                        cada solicitud. Tenga en cuenta que el conjunto de datos durante 
                        la sesión anónima se conserva cuando el usuario inicia sesión.
                        """
                        
                        login(request, user)

                        return render (request, "AppCoder/inicio.html", {"mensaje": f"Bienvenido/a {usuario}"})
                  else:
                        # Si ingresa aquí es por que hay algun tipo de error en los datos. 
                        # No existe el usuario
                        return render (request, "AppCoder/inicio.html", {"mensaje":"Error en los datos"})
            else:
                  # Si el formulario contiene errores ingresa a este else
                  # Se dirige al formulario a inicio.html y le pasamos el mensaje de error
                  # a Mostrar en la pantalla de inicio
                  return render(request, "AppCoder/inicio.html", {"mensaje":"Formulario erroneo"})
      
      #al final recuperamos el form
      # Si el medotodo no es POST debemos pensar que es la primera vez que se ingres a la vista
      # Por lo tanto se debe renderizar el formulariod de autenticación sin ningun valor en los campos
      form = AuthenticationForm()
    
      return render(request, "AppCoder/login.html", {'form': form})



def register(request):
      
      # Determinamos que el metodo de es POST es decir 
      #que los datos vienen en la solicitud de forma SEGURA
      if request.method == "POST":

            # Ya tenemos nuestro formulario predefinido de AUTH
            #form = UserCreationForm(request.POST)
            form = UserRegisterForm(request.POST)
            
            if form.is_valid():
                  
                  username = form.cleaned_data['username']
                  form.save()

                  return render(request, "AppCoder/inicio.html", {"mensaje": "usuario creado"})

      else: 
            form = UserRegisterForm()

      return render(request, "AppCoder/registro.html", {"form": form})


# def logout_request(request):
#       logout(request)
#       messages.info(request, "Saliste sin problemas")
#       return redirect("inicio")
     