from django.contrib import admin
from django.urls import path
from movie_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/directors/', views.director_list_api_view),
    path('api/v1/directors/<int:id>/', views.director_detail_api_view),
    path('api/v1/movies/', views.movie_list_api_view),
    path('api/v1/movies/<int:id>/', views.movie_detail_api_view),
    path('api/v1/reviews/', views.review_list_api_view),
    path('api/v1/reviews/<int:id>/', views.review_detail_api_view),
    path('api/v1/movies/reviews/', views.movie_reviews_api_view),
]

