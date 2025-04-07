from rest_framework import serializers
from .models import Productos

#Es una clase que actua sobre un modelo 
class productoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Productos
        fields = '__all__' #<-- Todos los campos
