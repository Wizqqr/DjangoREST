from django.contrib import admin
from django.urls import path, include
from movie_app import views as movie_views
from users import views as users_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/directors/', movie_views.director_list_create_api_view),
    path('api/v1/directors/<int:id>/', movie_views.director_detail_api_view),
    path('api/v1/movies/', movie_views.movie_list_api_view),
    path('api/v1/movies/<int:id>/', movie_views.movie_detail_api_view),
    path('api/v1/reviews/', movie_views.review_list_api_view),
    path('api/v1/reviews/<int:id>/', movie_views.review_detail_api_view),
    path('api/v1/movies/reviews/', movie_views.movie_reviews_api_view),
    path('api/v1/users/registration', users_views.registration_api_view),
    path('api/v1/users/authorization', users_views.authorization_api_view),
    path('api/v1/users/confirm', users_views.confirm_user_api_view)
]
