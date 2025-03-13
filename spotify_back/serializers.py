from rest_framework import serializers
from .models import User, Artist, Album, Song
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'username', 'date_of_birth', 'gender']
        extra_kwargs = {'password': {'write_only': True}}  

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = User(**validated_data)
        if password:
            user.set_password(password)  
        user.save()
        return user



class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=False, allow_blank=True)
    username = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        if not data.get("email") and not data.get("username"):
            raise serializers.ValidationError("Email or Username is required.")
        if not data.get("password"):
            raise serializers.ValidationError("Password is required.")
        return data



class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = '__all__'


class AlbumSerializer(serializers.ModelSerializer):
    artist = serializers.PrimaryKeyRelatedField(queryset=Artist.objects.all())  

    class Meta:
        model = Album
        fields = '__all__'

from rest_framework import serializers
from .models import Song

class SongSerializer(serializers.ModelSerializer):
    music_file_url = serializers.SerializerMethodField()
    fullscreen_image = serializers.ImageField(required=False)  

    class Meta:
        model = Song
        fields = [  
            'id', 'title', 'artist', 'album', 'image', 'music_file',
            'music_file_url', 'fullscreen_image', 'duration', 'plays'
        ]

    def get_music_file_url(self, obj):
        """Генерируем полный URL для аудиофайла"""
        request = self.context.get('request')
        return request.build_absolute_uri(obj.music_file.url) if obj.music_file else None





