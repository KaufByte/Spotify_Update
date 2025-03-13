from contextvars import Token
from django.shortcuts import render
from rest_framework import viewsets
from .models import User,Album,Song,Artist
from .serializers import UserSerializer,AlbumSerializer,SongSerializer,ArtistSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from django.contrib.auth import authenticate
from .serializers import LoginSerializer
from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer, LoginSerializer
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'])
    def login(self, request):
        """🔹 Авторизация по email/паролю"""
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = User.objects.get(email=email)
            if user.check_password(password):  # ✅ Проверяем пароль
                return Response({"message": "Login successful!", "email": user.email}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

    def update(self, request, *args, **kwargs):
        """Обновление артиста (PUT)"""
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """Частичное обновление артиста (PATCH)"""
        return super().partial_update(request, *args, **kwargs)


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

    def update(self, request, *args, **kwargs):
        """Обновление альбома (PUT)"""
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """Частичное обновление альбома (PATCH)"""
        return super().partial_update(request, *args, **kwargs)

class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    parser_classes = (MultiPartParser, FormParser) 

@api_view(['DELETE'])  # Разрешаем только DELETE-запросы
def delete_artist_by_id(request, artist_id):
    try:
        artist = Artist.objects.get(id=artist_id)
        artist.delete()
        return Response({"message": f"Artist with id {artist_id} deleted"}, status=status.HTTP_200_OK)
    except Artist.DoesNotExist:
        return Response({"error": "Artist not found"}, status=status.HTTP_404_NOT_FOUND)
    
