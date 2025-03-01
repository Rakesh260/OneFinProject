from rest_framework.views import APIView
from rest_framework.response import Response
from movie_collection.utils import MovieService, CollectionService
from movie_collection.serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from rest_framework.exceptions import ValidationError
from movie_collection.models import Collection, Movie


class RegisterUserView(APIView):

    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                return Response({'access_token': str(refresh.access_token)}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({"result": "failure", "message": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MovieListView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            movie_list = MovieService.fetch_movies()
            return Response({"result": "success", "data": movie_list}, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({"result": "failure", "message": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserMovieCollection(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            response_data = CollectionService.get_user_collection(request)
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({"result": "failure", "message": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            data = request.data
            get_movies = CollectionService.add_new_collection(request, data)
            return Response({"collection_uuid": get_movies}, status=status.HTTP_200_OK)
        except ValidationError as ve:
            return Response({"result": "failure", "message": ve.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({"result": "failure", "message": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CollectionDetailView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self,request, *args, **kwargs):
        try:
            collection_uuid = kwargs.get('collection_uuid')
            user_id = request.user.id
            response_data = CollectionService.get_collection_data_for_a_user(collection_uuid, user_id)
            return Response({"is_success": True, "data": response_data}, status=status.HTTP_200_OK)
        except Collection.DoesNotExist:
            return Response({"result": "failure", "message": "Collection not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            return Response({"result": "failure", "message": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self,request, *args, **kwargs):
        try:
            collection_uuid = kwargs.get('collection_uuid')
            user_id = request.user.id

            response_data = CollectionService.update_collection_data_for_a_user(request, collection_uuid, user_id)
            return Response({"is_success": True, "data": response_data}, status=status.HTTP_200_OK)

        except Collection.DoesNotExist:
            return Response({"result": "failure", "message": "Collection not found to update."}, status=status.HTTP_404_NOT_FOUND)
        except Movie.DoesNotExist:
            return Response({"result": "failure", "message": "One or more movies not found to update."},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            return Response({"result": "failure", "message": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self,request, *args, **kwargs):
        try:
            CollectionService.delete_collection(request, kwargs)
            return Response({"is_success": True, "message": "Collection deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Collection.DoesNotExist:
            return Response({"result": "failure", "message": "Collection not found to delete."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            return Response({"result": "failure", "message": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RequestCountView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        count = cache.get('request_count', 0)
        return Response({'requests': count}, status=status.HTTP_200_OK)


class ResetRequestCountView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        cache.set('request_count', 0)
        return Response({'message': 'request count reset successfully'}, status=status.HTTP_200_OK)

