from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import productoViewSet
from .views import *
#Definir un router
router = SimpleRouter()
router.register(r'api',productoViewSet)

#ProductoviewSet incluye:
#ip:80000/productos/api/ <--GET
#ip:80000/productos/api/{id} <--GET,POST,PUT,DELETE

urlpatterns = [
    path('',include(router.urls)),
    path('agregar/',agregar_producto, name='agregar'),
]
