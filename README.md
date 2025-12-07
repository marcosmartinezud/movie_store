# Movie Store

Small Django project with a simple movies app and a Vue-based contacts SPA.

## Setup (local)

1. Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

2. Apply migrations and create an admin user if needed:

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

3. Run the development server:

```powershell
python manage.py runserver
```

Open `http://127.0.0.1:8000/` to view the site.

## Contacts SPA

- Static SPA entry: `http://127.0.0.1:8000/static/contacts/index.html`
- The SPA talks to the JSON API under `/movies/api/contacts/`.
- CSRF is handled by reading the `csrftoken` cookie and sending `X-CSRFToken` headers. If you deploy the SPA separately, enable CORS and credentials as described below.

## API endpoints

- `GET /movies/api/contacts/` — list contacts
- `POST /movies/api/contacts/` — create contact (JSON body: `name`, `email`, `phone`)
- `DELETE /movies/api/contacts/<id>/` — delete contact

## Tests

Run the Django tests:

```powershell
python manage.py test movies
```

## CORS & CSRF

- `django-cors-headers` is included in `requirements.txt` and enabled in `settings.py`. `CORS_ALLOWED_ORIGINS` includes common local dev ports. `CORS_ALLOW_CREDENTIALS = True` is set so browsers can send cookies.
- The SPA uses `credentials: 'same-origin'` and `X-CSRFToken` headers for POST/DELETE. If you host the SPA on another origin, ensure the SPA runs on an allowed origin and sends credentials.

## Requirements

See `requirements.txt` for the Python dependencies used by this project.


