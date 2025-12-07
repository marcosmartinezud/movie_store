import json

from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods

from .models import Contact, Director, Genre, Movie

def home(request):
    genres = Genre.objects.all()
    latest_movies = {genre: genre.movies.last() for genre in genres}
    return render(request, 'movies/home.html', {'latest_movies': latest_movies})

def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'movies/movie_list.html', {'movies': movies})

def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    return render(request, 'movies/movie_detail.html', {'movie': movie})

def genre_list(request):
    genres = Genre.objects.all()
    return render(request, 'movies/genre_list.html', {'genres': genres})

def genre_detail(request, pk):
    genre = get_object_or_404(Genre, pk=pk)
    return render(request, 'movies/genre_detail.html', {'genre': genre})

def director_list(request):
    directors = Director.objects.all()
    return render(request, 'movies/director_list.html', {'directors': directors})

def director_detail(request, pk):
    director = get_object_or_404(Director, pk=pk)
    return render(request, 'movies/director_detail.html', {'director': director})


@require_http_methods(['GET', 'POST'])
def contact_api(request):
    if request.method == 'GET':
        contacts = list(Contact.objects.all().values('id', 'name', 'email', 'phone'))
        return JsonResponse(contacts, safe=False)

    try:
        payload = json.loads(request.body.decode('utf-8') or '{}')
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Invalid JSON payload')

    name = payload.get('name')
    email = payload.get('email')
    phone = payload.get('phone')

    if not all([name, email, phone]):
        return HttpResponseBadRequest('`name`, `email` and `phone` are required')

    contact = Contact.objects.create(name=name, email=email, phone=phone)
    return JsonResponse({'id': contact.id, 'name': contact.name, 'email': contact.email, 'phone': contact.phone}, status=201)


@require_http_methods(['DELETE'])
def contact_detail_api(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    contact.delete()
    return HttpResponse(status=204)
