"""
Configuracion WSGI para el proyecto movie_store.

Expone la aplicacion WSGI como variable de modulo ``application``.
Mas informacion: https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_store.settings')

application = get_wsgi_application()
