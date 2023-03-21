from dataclasses import fields
from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CursoFormulario(forms.Form):

    #Especificar los campos
    curso = forms.CharField()
    camada = forms.IntegerField()


class ProfesorFormulario(forms.Form):   
    nombre= forms.CharField(max_length=30)
    apellido= forms.CharField(max_length=30)
    email= forms.EmailField()
    profesion= forms.CharField(max_length=30)

class UserRegisterForm(UserCreationForm):
    
    # email = forms.EmailField()
    password1 = forms.CharField(label= 'Contraseña', widget= forms.PasswordInput)
    password2 = forms.CharField(label= 'Repita la contraseña', widget=forms.PasswordInput)


    # La Clase meta me permite hablar de los metadatos 
    
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        # Elimina los mensajes de ayuda 
        help_texts= {k:"" for k in fields}