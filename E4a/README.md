# Movie Store (E4a)

Proyecto Django con la app de películas propuesta en la asignatura.

## Requisitos

- Python 3.13+ (probado con 3.13)
- Dependencias en `requirements.txt`

## Puesta en marcha

```bash
cd E4a
python -m pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser   # opcional
python manage.py runserver
```

Sitio principal: `http://127.0.0.1:8000/`

## Datos de ejemplo

```bash
cd E4a
python manage.py shell < add_sample_data.py
```

## Tests

```bash
cd E4a
python manage.py test movies
```
