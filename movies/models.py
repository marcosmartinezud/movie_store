from django.db import models

class Director(models.Model):
    name = models.CharField(max_length=100)
    biography = models.TextField()
    birth_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    
    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=200)
    release_year = models.IntegerField()
    description = models.TextField()
    poster = models.URLField(blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='movies')
    directors = models.ManyToManyField(Director, related_name='movies')
    
    def __str__(self):
        return self.title
