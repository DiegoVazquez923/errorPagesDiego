#Define formularios de los modelos en esta app
from django import forms
from .models import Categoria

#crear una clase para cada modelo
class categoriaForm(forms.ModelForm):
    #Meta es la clase que mide la meta informacion del formulario
    class Meta:
        #De que modelo se basa este formulario
        model = Categoria

        #Saber que campos se van a ver en le formulario
        fields= ['nombre','imagen']
        
        #Personalizar la apariencia del formulario (widgets)
        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-input',
                    'placeholder': 'Nombre de la categoria'
                }
            ),
            'imagen': forms.URLInput(
                attrs={
                    'class': 'form-input',
                    'placeholder':'Imagen de la categoria'
                }
            )
        }

        #personalizar las etiquetas
        labels={
            'nombre':'Nombre de la categoria',
            'imagen':'URL de la imagen'
        }

        #Mensajes de error
        error_messages={
            'nombre':{
                'required':'El nombre es obligatorio'
            },
        }