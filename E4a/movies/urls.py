from django.urls import path
from . import views

app_name = 'movies'
# Rutas principales del catalogo y paginas auxiliares
urlpatterns = [
    path('', views.home, name='home'),
    path('movies/', views.MovieListView.as_view(), name='movie_list'),
    path('movies/add/', views.MovieCreateView.as_view(), name='movie_create'),
    path('movies/<int:pk>/', views.MovieDetailView.as_view(), name='movie_detail'),
    path('movies/<int:pk>/edit/', views.MovieUpdateView.as_view(), name='movie_edit'),
    path('movies/<int:pk>/delete/', views.MovieDeleteView.as_view(), name='movie_delete'),
    path('movies/<int:pk>/ajax-delete/', views.movie_delete_api, name='movie_ajax_delete'),  # Usado por fetch en el listado
    path('genres/', views.genre_list, name='genre_list'),
    path('genres/<int:pk>/', views.genre_detail, name='genre_detail'),
    path('directors/', views.director_list, name='director_list'),
    path('directors/<int:pk>/', views.director_detail, name='director_detail'),
]
