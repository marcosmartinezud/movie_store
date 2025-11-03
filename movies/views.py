from django.shortcuts import render, get_object_or_404
from .models import Movie, Director, Genre

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
