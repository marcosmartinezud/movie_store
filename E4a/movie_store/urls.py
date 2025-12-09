"""
Configuracion de URLs para el proyecto movie_store.

`urlpatterns` reparte las rutas hacia las vistas que tocan.
Mas detalles: https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('movies.urls')),
]
