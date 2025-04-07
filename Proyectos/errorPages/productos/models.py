from django.db import models
from categorias.models import Categoria
# Create your models here.

class Productos(models.Model):
    #Aqui van los atributos de mi clase
    nombre=models.CharField(max_length=100)
    precio=models.DecimalField(max_digits=10,decimal_places=2)
    #los URLFields se limitan a 200 caracteres
    imagen=models.URLField()
    
    #Agregaar relacion con categoria
    #Parametros: Modelo, (opc) opcion para borrar el producto si está relacionado
    categoria= models.ForeignKey(
        Categoria,
        on_delete = models.SET_NULL,
        null = True,
        blank = True
    )

    #lo que se va a devolver al hacer llamada a Productos
    def __str__(self):
        return self.nombre
