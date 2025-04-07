from django.db import models

# Create your models here.

class Categoria(models.Model):
    #Aqui van los atributos de mi clase
    nombre=models.CharField(max_length=100)
    #los URLFields se limitan a 200 caracteres
    imagen=models.URLField()
    
    #lo que se va a devolver al hacer llamada a Productos
    def __str__(self):
        return self.nombre
