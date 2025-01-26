from django.shortcuts import render
from app.services.movies.movie_list import MovieService
from app.services.movies.movie_detail import MovieDetailService
from django.conf import settings
import requests

def home(request):
  return render(request, 'home.html')

def tv_detail(request, movie_id):
    movie_service = MovieDetailService()
    content_type = request.GET.get('type', 'tv')

    movie_data = movie_service.fetch_movie_details(movie_id, content_type)
    return render(request, f"{content_type}_detail.html", {'movie': movie_data})

def movie_detail(request, movie_id):
    movie_service = MovieDetailService()
    content_type = request.GET.get('type', 'movie')

    movie_data = movie_service.fetch_movie_details(movie_id, content_type)
    return render(request, f"{content_type}_detail.html", {'movie': movie_data})

def tv_list(request):
    content_type = request.GET.get('type', 'tv')
    movie_service = MovieService()
    context = movie_service.fetch_movies(
        order_by=request.GET.get('order', 'desc'),
        sort=request.GET.get('sort_by', 'popularity'),
        search_query=request.GET.get('search', ''),
        page=int(request.GET.get('page', 1)),
        content_type=content_type,
    )
    return render(request, f"list_{content_type}.html", context)

def movie_list(request):
    content_type = request.GET.get('type', 'movie')
    movie_service = MovieService()
    context = movie_service.fetch_movies(
        order_by=request.GET.get('order', 'desc'),
        sort=request.GET.get('sort_by', 'popularity'),
        search_query=request.GET.get('search', ''),
        page=int(request.GET.get('page', 1)),
        content_type=content_type,
    )

    return render(request, f"list_{content_type}.html", context)