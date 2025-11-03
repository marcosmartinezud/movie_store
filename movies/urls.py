from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    path('', views.home, name='home'),
    path('movies/', views.movie_list, name='movie_list'),
    path('movies/<int:pk>/', views.movie_detail, name='movie_detail'),
    path('genres/', views.genre_list, name='genre_list'),
    path('genres/<int:pk>/', views.genre_detail, name='genre_detail'),
    path('directors/', views.director_list, name='director_list'),
    path('directors/<int:pk>/', views.director_detail, name='director_detail'),
]