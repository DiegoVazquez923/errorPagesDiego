#Define formularios de los modelos en esta app
from django import forms
from .models import Productos

#crear una clase para cada modelo
class productoForm(forms.ModelForm):
    #Meta es la clase que mide la meta informacion del formulario
    class Meta:
        #De que modelo se basa este formulario
        model = Productos

        #Saber que campos se van a ver en le formulario
        fields= ['nombre','precio','imagen','categoria']
        
        #Personalizar la apariencia del formulario (widgets)
        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-input',
                    'placeholder': 'Nombre del prducto'
                }
            ),
            'precio': forms.NumberInput(
                attrs={
                    'class': 'form-input',
                    'placeholder':'Precio del producto'
                }
            ),
            'imagen': forms.URLInput(
                attrs={
                    'class': 'form-input',
                    'placeholder':'Imagen del producto'
                }
            ),
            'categoria': forms.Select(
                attrs={
                    'class': 'form-input',
                }
            ),
        }

        #personalizar las etiquetas
        labels={
            'nombre':'Nombre del producto',
            'precio':'Precio (MXN)',
            'imagen':'URL de la imagen',
            'categoria':'Categoria del producto',
        }

        #Mensajes de error
        error_messages={
            'nombre':{
                'required':'El nombre es obligatorio'
            },
            'precio':{
                'required': 'El precio no debe estar vacio',
                'invalid': 'Invalido'
            }
        }