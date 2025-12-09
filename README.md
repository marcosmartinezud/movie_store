# Movie Store – Entrega E4

Repositorio dividido en dos carpetas independientes:

- `E4a/` — Proyecto Django (app de películas + API de contactos). Ver `E4a/README.md` para pasos de instalación y datos de ejemplo.
- `E4b/contacts-spa/` — SPA en Vue 3 para la agenda de contactos lista para servir de forma estática.

## Arranque rápido

- Backend (E4a): `cd E4a && python -m pip install -r requirements.txt && python manage.py migrate && python manage.py runserver`
- SPA (E4b): `cd E4b/contacts-spa && python -m http.server 5173` y abre `http://127.0.0.1:5173/`.
