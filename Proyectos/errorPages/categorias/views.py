from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Categoria   
from .forms import categoriaForm
import json

# Create your views here.
def agregar_categoria(request):
    #Checar si vengo desde el formulario enviado
    if request.method=='POST':
        #Mandaron el formulario
        form = categoriaForm(request.POST)

        #validar formulario correcto
        if form.is_valid():
            form.save()
            return redirect('json') #redireccion a la lista de categorias
    else:
        form= categoriaForm()
    #pintar formulario
    return render(request,'registrar.html', {'form': form})    

def registrar_categoria(request):
    if request.method == 'POST':
        try:
            data=json.loads(request.body) #toma crudo y lo hace json
            categoria= Categoria.objects.create(
                nombre=data['nombre'],
                imagen=data['imagen']
            )
            return JsonResponse({
                    'mensaje':'Registro exitoso',
                    'id':categoria.id
                },status=201)
        except Exception as e:
            return JsonResponse({
                'Error':'Ocurrio un error' + str(e)
            },status=400)
    return JsonResponse({
        'Error':'Metodo no soportado'
    }, status=405)

def ver_categoria(request): 
    #Obtener de la BD todos los categorias
    categorias = Categoria.objects.all()

    return render(request,'json.html',{'categorias':categorias})

#Funcion que pinta la carga de categorias co json
def index(request):
    return render(request,'categoria.html')

#Devuelve todos los categorias como un json
def lista_categorias(request):
    categorias= Categoria.objects.all()

    #diccionario al aire  que ordene los categorias
    data= [
        {
            'nombre': c.nombre,
            'imagen': c.imagen
        }
        for c in categorias
    ]
    return JsonResponse(data, safe=False)