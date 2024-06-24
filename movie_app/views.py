from django.db.models import Count, Avg
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import DirectorSerializer, MovieSerializer, ReviewSerializer
from .models import Director, Movie, Review

@api_view(['GET', 'POST'])
def director_list_create_api_view(request):
    print(request.user)
    if request.method == 'GET':
        directors = Director.objects.annotate(movies_count=Count('movies'))
        serialized_data = DirectorSerializer(directors, many=True).data
        return Response(data=serialized_data)
    elif request.method == 'POST':
        serializer = DirectorSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data={'errors':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        name = request.data.get('name')
        print(name)

        director = Director.objects.create(name=name)
        return Response(data={'director_id': director.id, 'name': director.name}, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def director_detail_api_view(request, id):
    try:
        director = Director.objects.annotate(movies_count=Count('movies')).get(id=id)
    except Director.DoesNotExist:
        return Response(data={'error': 'Director not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = DirectorSerializer(director).data
        return Response(data=data)
    elif request.method == 'DELETE':
        director.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = DirectorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        director.name = request.data.get('name')
        director.save()
        return Response(status=status.HTTP_201_CREATED)


# API для списка и создания фильмов
@api_view(['GET', 'POST'])
def movie_list_api_view(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        serialized_data = MovieSerializer(movies, many=True).data
        return Response(data=serialized_data)
    elif request.method == 'POST':
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def movie_detail_api_view(request, id):
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(data={'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = MovieSerializer(movie).data
        return Response(data=data)
    elif request.method == 'DELETE':
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = MovieSerializer(movie, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
def movie_reviews_api_view(request):
    movies = Movie.objects.annotate(avg_rating=Avg('reviews__stars')).prefetch_related('reviews')
    serialized_data = MovieSerializer(movies, many=True).data
    return Response(data=serialized_data)


@api_view(['GET', 'POST'])
def review_list_api_view(request):
    if request.method == 'GET':
        data = Review.objects.all()
        list_ = ReviewSerializer(data, many=True).data
        return Response(data=list_)
    elif request.method == 'POST':
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ReviewSerializer(review).data
        return Response(data=data)
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = ReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review.text = request.data.get('text')
        review.movie_id = request.data.get('movie')
        review.stars = request.data.get('stars')
        review.save()
        return Response(status=status.HTTP_201_CREATED)