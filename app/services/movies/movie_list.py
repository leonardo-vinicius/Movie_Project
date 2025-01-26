# services/movie_service.py
import requests
from django.conf import settings

class MovieService:
    def __init__(self, api_key=settings.TMDB_API_KEY):
        self.base_url = 'https://api.themoviedb.org/3'
        self.api_key = api_key

    def _prepare_params(self, order_by='desc', sort='popularity', search_query='', page=1):
        params = {
            'api_key': self.api_key,
            'sort_by': f"{sort}.{order_by}",
            'page': page
        }
        
        if search_query:
            params['query'] = search_query
        
        return params

    def _process_movies(self, movies, release):
        for movie in movies:
            movie[release] = movie.get(release, 'N/A').split("-")[0] if movie.get(release) else "N/A"
            movie['vote_average'] = round(float(movie.get('vote_average', 0)), 1)
            for key, value in movie.items():
                if isinstance(value, bool):
                    movie[key] = str(value).lower()
        return movies


    def fetch_movies(self, order_by='desc', sort='popularity', search_query='', page=1, content_type='movie'):
        url = f"{self.base_url}/search/{content_type}" if search_query else f"{self.base_url}/discover/{content_type}"
        params = self._prepare_params(order_by, sort, search_query, page)

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            movies = data.get('results', [])
            has_next_page = page < data.get('total_pages', float('inf'))
            
            release = 'release_date' if content_type == 'movie' else 'first_air_date'

            processed_movies = self._process_movies(movies, release)
            
            return {
                'movies': processed_movies,
                'page': page,
                'has_next_page': has_next_page,
                'search_query': search_query,
            }

        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar: {e}")
            return {
                'movies': [],
                'page': page,
                'has_next_page': False,
                'search_query': search_query,
            }