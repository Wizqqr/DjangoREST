from django.contrib import admin
from django.urls import path, include
from movie_app import views as movie_views
from users import views as users_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/directors/', movie_views.DirectorListApiView.as_view()),
    path('api/v1/directors/<int:id>/', movie_views.DirectorDetailApiView.as_view()),
    path('api/v1/movies/', movie_views.MovieListApiView.as_view()),
    path('api/v1/movies/<int:id>/', movie_views.MovieDetailApiView.as_view()),
    path('api/v1/reviews/', movie_views.ReviewListApiView.as_view()),
    path('api/v1/reviews/<int:id>/', movie_views.ReviewDetailApiView.as_view()),
    path('api/v1/movies/reviews/', movie_views.MovieReviewsApiView.as_view()),
    path('api/v1/users/registration', users_views.RegistrationApiView.as_view()),
    path('api/v1/users/authorization', users_views.AuthenficationApiView.as_view()),
    path('api/v1/users/confirm', users_views.ConfirmApiView.as_view()),
]
