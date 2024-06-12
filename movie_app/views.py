from django.db.models import Count, Avg
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import DirectorSerializer, MovieSerializer, ReviewSerializer
from .models import Director, Movie, Review

@api_view(['GET'])
def director_list_api_view(request):
    directors = Director.objects.annotate(movies_count=Count('movies'))
    serialized_data = DirectorSerializer(directors, many=True).data
    return Response(data=serialized_data)

@api_view(['GET'])
def director_detail_api_view(request, id):
    try:
        director = Director.objects.annotate(movies_count=Count('movies')).get(id=id)
    except Director.DoesNotExist:
        return Response(data={'error': 'Director not found'}, status=status.HTTP_404_NOT_FOUND)
    data = DirectorSerializer(director).data
    return Response(data=data)

@api_view(['GET'])
def movie_list_api_view(request):
    data = Movie.objects.all()
    list_ = MovieSerializer(data, many=True).data
    return Response(data=list_)

@api_view(['GET'])
def movie_detail_api_view(request, id):
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(data={'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
    data = MovieSerializer(movie).data
    return Response(data=data)

@api_view(['GET'])
def movie_reviews_api_view(request):
    movies = Movie.objects.annotate(
        avg_rating=Avg('reviews__stars')
    ).prefetch_related('reviews')
    serialized_data = MovieSerializer(movies, many=True).data
    return Response(data=serialized_data)

@api_view(['GET'])
def review_list_api_view(request):
    data = Review.objects.all()
    list_ = ReviewSerializer(data, many=True).data
    return Response(data=list_)

@api_view(['GET'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)
    data = ReviewSerializer(review).data
    return Response(data=data)
