from django.urls import path
from .views import *

urlpatterns=[
    path('registrar/',agregar_categoria, name='registrar'),
    path('json/',ver_categoria,name='json'),
    path('',index,name='home'),
    path('api/get/',lista_categorias,name='lista'),     
    path("api/post/",registrar_categoria,name='post'),
]