from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

class Director(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return  self.name

    class Meta:
        verbose_name = "Director"
        verbose_name_plural = "Directors"



class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    duration = models.IntegerField()
    director = models.ForeignKey(Director, related_name='movies', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Review(models.Model):
    text = models.CharField(max_length=100)
    movie = models.ForeignKey(Movie, related_name='reviews', on_delete=models.CASCADE)
    stars = models.PositiveIntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(5)], null=True)

    def __str__(self):
        return self.text