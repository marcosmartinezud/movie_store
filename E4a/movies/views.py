from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.http import require_http_methods, require_POST
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.utils.decorators import method_decorator

from .forms import MovieForm
from .models import Director, Genre, Movie


def home(request):
    # Toma el ultimo titulo de cada genero para mostrar un resumen en portada
    genres = Genre.objects.all()
    latest_movies = {genre: genre.movies.last() for genre in genres}
    return render(request, 'movies/home.html', {'latest_movies': latest_movies})


@method_decorator(ensure_csrf_cookie, name='dispatch')
class MovieListView(ListView):
    """Lista todas las peliculas en la tabla Movie."""
    model = Movie
    template_name = 'movies/movie_list.html'
    context_object_name = 'movies'


class MovieDetailView(DetailView):
    """Muestra la ficha completa de una pelicula concreta."""
    model = Movie
    template_name = 'movies/movie_detail.html'
    context_object_name = 'movie'


class MovieCreateView(CreateView):
    """Formulario para crear una pelicula nueva."""
    model = Movie
    form_class = MovieForm
    template_name = 'movies/movie_form.html'

    def get_success_url(self):
        # Tras guardar redirige a la pagina de detalle de la pelicula creada
        return reverse('movies:movie_detail', kwargs={'pk': self.object.pk})


class MovieDeleteView(DeleteView):
    """Borra una pelicula desde el flujo tradicional con confirmacion."""
    model = Movie
    template_name = 'movies/movie_confirm_delete.html'
    context_object_name = 'movie'
    success_url = reverse_lazy('movies:movie_list')


@require_POST
def movie_delete_api(request, pk):
    # Endpoint usado por AJAX para borrar sin recargar la pagina
    movie = get_object_or_404(Movie, pk=pk)
    movie.delete()
    return JsonResponse({'id': pk, 'deleted': True})


class MovieUpdateView(UpdateView):
    """Edita una pelicula existente reutilizando el mismo formulario."""
    model = Movie
    form_class = MovieForm
    template_name = 'movies/movie_form.html'

    def get_success_url(self):
        return reverse('movies:movie_detail', kwargs={'pk': self.object.pk})

def genre_list(request):
    # Listado general de generos para navegar entre ellos
    genres = Genre.objects.all()
    return render(request, 'movies/genre_list.html', {'genres': genres})

def genre_detail(request, pk):
    # Vista de detalle con las peliculas asociadas a un genero
    genre = get_object_or_404(Genre, pk=pk)
    return render(request, 'movies/genre_detail.html', {'genre': genre})

def director_list(request):
    # Recoge todos los directores para mostrarlos con conteo de peliculas
    directors = Director.objects.all()
    return render(request, 'movies/director_list.html', {'directors': directors})

def director_detail(request, pk):
    # Perfil de un director con la filmografia que tiene en la base de datos
    director = get_object_or_404(Director, pk=pk)
    return render(request, 'movies/director_detail.html', {'director': director})
