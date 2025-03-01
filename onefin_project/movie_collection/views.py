from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
# from movie_collection.manager import UserManagement, CollectionManagement
from movie_collection.serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status


class RegisterUserView(APIView):

    def post(self,request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                return Response({'access_token': str(refresh.access_token)}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({"result": "failure", "message": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)