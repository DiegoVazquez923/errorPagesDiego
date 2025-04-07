from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Productos   
from .forms import productoForm
import json

# Create your views here.
def agregar_producto(request):
    #Checar si vengo desde el formulario enviado
    if request.method=='POST':
        #Mandaron el formulario
        form = productoForm(request.POST)

        #validar formulario correcto
        if form.is_valid():
            form.save()
            return redirect('ver') #redireccion a la lista de productos
    else:
        form= productoForm()
    #pintar formulario
    return render(request,'agregar.html', {'form': form})    

#Funcion agregar producto con llamada asincrona

#evitar csrf
#@csrf_exempt <-- Evitar a menos que solo se esté probando
def registrar_producto(request):
    if request.method == 'POST':
        try:
            data=json.loads(request.body) #toma crudo y lo hace json
            producto= Productos.objects.create(
                nombre=data['nombre'],
                precio=data['precio'],
                imagen=data['imagen']
            )
            return JsonResponse({
                    'mensaje':'Registro exitoso',
                    'id':producto.id
                },status=201)
        except Exception as e:
            return JsonResponse({
                'Error':'Ocurrio un error' + str(e)
            },status=400)
    return JsonResponse({
        'Error':'Metodo no soportado'
    }, status=405)

def ver_producto(request):
    #Obtener de la BD todos los productos
    productos = Productos.objects.all()

    return render(request,'ver.html',{'productos':productos})

#Funcion que pinta la carga de productos co json
def index(request):
    return render(request,'productos.html')

#Devuelve todos los productos como un json
def lista_productos(request):
    productos= Productos.objects.all()

    #diccionario al aire  que ordene los productos
    data= [
        {
            'nombre': p.nombre,
            'precio': p.precio,
            'imagen': p.imagen
        }
        for p in productos
    ]
    return JsonResponse(data, safe=False)