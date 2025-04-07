from django.shortcuts import render
from rest_framework import viewsets
from  rest_framework.renderers import JSONRenderer
from .models import Alumno
from .serializers import alumnoSerializer
from .forms import alumnoForm

class alumnoViewSet(viewsets.ModelViewSet):
    queryset = Alumno.objects.all() #<-- Conjunto de querys de la bd
    serializer_class = alumnoSerializer #-- Empaquetar y enviar la informacion
    renderer_classes = [JSONRenderer] #<-- Saber como renderizar la respuesta
    
def ver_alumnos(request): 
    form = alumnoForm(request.POST)
    return render(request,'Diego_Vazquez.html',{'form': form})
