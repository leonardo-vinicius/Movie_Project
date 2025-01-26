from django.urls import path
from . import views
from app.views import movie_list, movie_detail, tv_detail, tv_list

urlpatterns = [
    path("api/movie_list", movie_list, name="movie_list"),
    path("api/tv_list", tv_list, name="tv_list"),
    path('movie/<int:movie_id>/', movie_detail, name='movie_detail'),
    path('tv/<int:movie_id>/', tv_detail, name='tv_detail'),
    ]
