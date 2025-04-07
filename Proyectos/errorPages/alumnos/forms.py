#Define formularios de los modelos en esta app
from django import forms
from .models import Alumno

#crear una clase para cada modelo
class alumnoForm(forms.ModelForm):
    #Meta es la clase que mide la meta informacion del formulario
    class Meta:
        #De que modelo se basa este formulario
        model = Alumno

        #Saber que campos se van a ver en le formulario
        fields= ['nombre','apellido',"edad",'matricula','correo']
        
        #Personalizar la apariencia del formulario (widgets)
        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-input',
                    'placeholder': 'Nombre del alumno'
                }
            ),
            'apellido': forms.TextInput(
                attrs={
                    'class': 'form-input',
                    'placeholder': 'Apellido del alumno'
                }
            ),
            'edad': forms.NumberInput(
                attrs={
                    'class': 'form-input',
                    'placeholder': 'Edad'
                }
            ),
            'matricula': forms.TextInput(
                attrs={
                    'class': 'form-input',
                    'placeholder': 'Matricua'
                }
            ),
            'correo': forms.EmailInput(
                attrs={
                    'class': 'form-input',
                    'placeholder': 'Correo electrónico del alumno'
                }
            ),
        }
        labels={
            'nombre':'',
            'apellido':'',
            'edad':''
        }
