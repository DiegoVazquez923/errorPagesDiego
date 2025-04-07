from rest_framework import viewsets
from  rest_framework.renderers import JSONRenderer
from .models import Productos
from .serializers import productoSerializer
from .forms import productoForm
from django.shortcuts import render,redirect

class productoViewSet(viewsets.ModelViewSet):
    queryset = Productos.objects.all() #<-- Conjunto de querys de la bd
    serializer_class = productoSerializer #-- Empaquetar y enviar la informacion
    renderer_classes = [JSONRenderer] #<-- Saber como renderizar la respuesta

    #http_method_names = ['GET','POST']  #  Esta variable es para unicamente tener ciertos metodos
    
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

