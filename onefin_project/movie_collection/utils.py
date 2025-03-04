import requests
import time
from decouple import config
from movie_collection.models import Collection, Movie, CollectionMap
from collections import Counter
from django.db import transaction
from rest_framework.exceptions import ValidationError
from movie_collection.serializers import MovieSerializer

MOVIE_API_USERNAME = config('MOVIE_API_USERNAME')
MOVIE_API_PASSWORD = config('MOVIE_API_PASSWORD')


class MovieService:

    @staticmethod
    def fetch_movies(retries=3, delay=2):

        url = 'https://demo.credy.in/api/v1/maya/movies/'
        headers = {
            'Username': MOVIE_API_USERNAME,
            'Password': MOVIE_API_PASSWORD
        }

        for attempt in range(retries):
            try:
                response = requests.get(url, headers=headers, verify=True)
                response.raise_for_status()
                return response.json()

            except requests.exceptions.Timeout as error:
                print(f"Attempt {attempt + 1}: Connection timed out. Retrying...: {error}")

            except requests.exceptions.RequestException as error:
                print(f"Attempt {attempt + 1}: Exception occurred: {error}")
            time.sleep(delay)
        raise Exception(f"Failed to connect after {retries} attempts.")


class CollectionService:

    @staticmethod
    def get_user_collection(request):
        user_id = request.user.id
        collections, favourite_genres = CollectionService.get_collection_by_user_id(user_id)
        collection_data = [
            {
                "title": collection.title,
                "uuid": str(collection.uuid),
                "description": collection.description
            }
            for collection in collections
        ]

        response_data = {
            "is_success": True,
            "data": {
                "collections": collection_data,
                "favourite_genres": favourite_genres
            }
        }
        return response_data

    @staticmethod
    def get_collection_by_user_id(user_id):
        collections_objs = Collection.objects.filter(user=user_id).prefetch_related('movies__movie_key')
        genres = []
        for collection in collections_objs:
            for mapping in collection.movies.all():
                if mapping.movie_key and mapping.movie_key.genres:
                    non_empty_genres = [genre.strip() for genre in mapping.movie_key.genres.split(',') if genre.strip()]
                    genres.extend(non_empty_genres)
        genre_counts = Counter(genres)
        top_genres = genre_counts.most_common(3)
        favourite_genres = [genre for genre, count in top_genres]
        return collections_objs, favourite_genres

    @staticmethod
    def add_new_collection(request, data):
        user_id = request.user.id
        title = data.get('title')
        description = data.get('description')
        movies = data.get('movies')
        if not title:
            raise ValidationError("Title is missing")
        if not description:
            raise ValidationError("Description is missing")
        if not movies:
            raise ValidationError("Movies are missing")

        with transaction.atomic():
            if Collection.objects.filter(title__iexact=title, user=user_id).exists():
                raise Exception("A collection with this title already exists.")

            collection = Collection.objects.create(
                title=title,
                user=request.user,
                description=description
            )
            for movie_data in movies:
                movie, created = Movie.objects.get_or_create(
                    uuid=movie_data['uuid'],
                    defaults={
                        'title': movie_data['title'],
                        'description': movie_data['description'],
                        'genres': movie_data['genres']
                    }
                )
                CollectionMap.objects.create(collection_key=collection, movie_key=movie)
            return collection.uuid

    @staticmethod
    def get_collection_data_for_a_user(collection_uuid, user_id):
        collection = Collection.objects.get(uuid=collection_uuid, user=user_id)
        collection_mappings = CollectionMap.objects.filter(collection_key=collection).select_related('movie_key')
        movies = [mapping.movie_key for mapping in collection_mappings]
        movie_details = MovieSerializer(movies, many=True).data
        response_data = {
            "title": collection.title,
            "description": collection.description,
            "movies": movie_details,
        }
        return response_data

    @staticmethod
    def update_collection_data_for_a_user(request, collection_uuid, user_id):
        collection = Collection.objects.get(uuid=collection_uuid, user=user_id)
        with transaction.atomic():
            collection.title = request.data.get('title', collection.title)
            collection.description = request.data.get('description', collection.description)
            collection.save()
            movie_uuids = [movie['uuid'] for movie in request.data.get('movies', [])]
            current_movies = CollectionMap.objects.filter(collection_key=collection).select_related('movie_key')
            current_movie_uuids = [str(mapping.movie_key.uuid) for mapping in current_movies]
            for mapping in current_movies:
                if str(mapping.movie_key.uuid) not in movie_uuids:
                    mapping.delete()
            for movie_uuid in movie_uuids:
                if movie_uuid not in current_movie_uuids:
                    movie = Movie.objects.get(uuid=movie_uuid)
                    CollectionMap.objects.create(collection_key=collection, movie_key=movie)

            updated_movies = CollectionMap.objects.filter(collection_key=collection).select_related('movie_key')
            movie_details = MovieSerializer([mapping.movie_key for mapping in updated_movies], many=True).data

            response_data = {
                "title": collection.title,
                "description": collection.description,
                "movies": movie_details,
            }

            return response_data

    @staticmethod
    def delete_collection(request, kwargs):
        user_id = request.user.id
        collection_uuid = kwargs.get('collection_uuid')
        collection = Collection.objects.get(uuid=collection_uuid, user=user_id)
        collection.delete()
