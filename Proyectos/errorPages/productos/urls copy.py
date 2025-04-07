from django.urls import path
from .views import *

urlpatterns=[
    path('agregar/',agregar_producto, name='agregar'),
    path('ver/',ver_producto,name='ver'),
    path('',index,name='home'),
    path('api/get/',lista_productos,name='lista'),
    path("api/post/",registrar_producto,name='post')
]