# services/movie_detail_service.py
import requests
from django.conf import settings

class MovieDetailService:
    def __init__(self, api_key=None):
        self.api_key = api_key or settings.TMDB_API_KEY
        self.base_url = 'https://api.themoviedb.org/3'

    def fetch_movie_details(self, movie_id, content_type):
        url = f"{self.base_url}/{content_type}/{movie_id}"
        
        params = {
            'api_key': self.api_key,
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            movie_data = response.json()

            movie_data['release_year'] = movie_data.get('release_date', '')[:4] if movie_data.get('release_date') else ''
            movie_data['vote_average'] = round(movie_data.get('vote_average', 0), 1)

            return movie_data

        except requests.exceptions.RequestException as e:
            print(f"Error fetching movie details: {e}")
            return None