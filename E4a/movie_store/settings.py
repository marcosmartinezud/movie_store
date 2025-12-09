"""
Configuracion de Django para el proyecto movie_store.

Generado por 'django-admin startproject' con Django 5.2.7.

Mas informacion sobre este archivo:
https://docs.djangoproject.com/en/5.2/topics/settings/

Listado completo de opciones y valores:
https://docs.djangoproject.com/en/5.2/ref/settings/
"""

from pathlib import Path

# Rutas base del proyecto, p.e. BASE_DIR / 'subdir'
BASE_DIR = Path(__file__).resolve().parent.parent


# Ajustes rapidos de desarrollo, no validos para produccion
# Ver https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# Advertencia: mantiene esta clave secreta a salvo en produccion
SECRET_KEY = 'django-insecure-nd+ht@0273h=jcs7@_y+wkbsv%muy61!#-rp^pt+eiie)3@z3r'

# Advertencia: no ejecutes con DEBUG activo en produccion
DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '::1',
    'testserver',  # habilitar host del cliente de pruebas
]


# Definicion de aplicaciones instaladas

INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'movies',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'movie_store.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'movie_store.wsgi.application'


# Base de datos
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Validacion de contrasenas
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internacionalizacion
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Archivos estaticos (CSS, JS, imagenes)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Tipo de clave primaria por defecto
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOWED_ORIGINS = [
    'http://localhost',
    'http://127.0.0.1',
    'http://localhost:5173',
    'http://127.0.0.1:5173',
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]

CORS_ALLOW_CREDENTIALS = True

# Permitir despliegues estáticos en Netlify para la SPA (E4b)
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://.*\\.netlify\\.app$",
]
