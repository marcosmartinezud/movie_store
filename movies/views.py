import json

from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.http import require_http_methods, require_POST
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .models import Contact, Director, Genre, Movie


def home(request):
    genres = Genre.objects.all()
    latest_movies = {genre: genre.movies.last() for genre in genres}
    return render(request, 'movies/home.html', {'latest_movies': latest_movies})


@ensure_csrf_cookie
def contacts_spa(request):
    return render(request, 'movies/contacts_spa.html')


class MovieListView(ListView):
    model = Movie
    template_name = 'movies/movie_list.html'
    context_object_name = 'movies'


class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movies/movie_detail.html'
    context_object_name = 'movie'


class MovieCreateView(CreateView):
    model = Movie
    fields = ['title', 'release_year', 'description', 'poster', 'genre', 'directors']
    template_name = 'movies/movie_form.html'

    def get_success_url(self):
        return reverse('movies:movie_detail', kwargs={'pk': self.object.pk})


class MovieDeleteView(DeleteView):
    model = Movie
    template_name = 'movies/movie_confirm_delete.html'
    context_object_name = 'movie'
    success_url = reverse_lazy('movies:movie_list')


@require_POST
def movie_delete_api(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    movie.delete()
    return JsonResponse({'id': pk, 'deleted': True})


class MovieUpdateView(UpdateView):
    model = Movie
    fields = ['title', 'release_year', 'description', 'poster', 'genre', 'directors']
    template_name = 'movies/movie_form.html'

    def get_success_url(self):
        return reverse('movies:movie_detail', kwargs={'pk': self.object.pk})

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
