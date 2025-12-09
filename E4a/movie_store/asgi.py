"""
Configuracion ASGI para el proyecto movie_store.

Expone la llamada ASGI como variable de modulo llamada ``application``.
Mas informacion: https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_store.settings')

application = get_asgi_application()
