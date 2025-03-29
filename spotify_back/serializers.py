from rest_framework import serializers
from .models import User, Artist, Album, Song
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'username', 'date_of_birth', 'gender','subscribed_artists','favorite_songs']
        extra_kwargs = {'password': {'write_only': True}}  

    def create(self, validated_data):
        subscribed_artists_data = validated_data.pop('subscribed_artists',[])
        favorite_songs_data = validated_data.pop('favorite_songs',[])
        password = validated_data.pop("password", None)
        user = User(**validated_data)
        if password:
            user.set_password(password)  
        user.save()

        user.subscribed_artists.set(subscribed_artists_data)
        user.favorite_songs.set(favorite_songs_data)
        user.save()
        return user

    def update(self,instance,validate_data):
        subscribed_artists_data = validate_data.pop('subscribed_artists',None)
        favorite_songs_data = validate_data.pop('favorite_songs_data', None)

        if 'password' in validate_data:
            password = validate_data.pop('password')
            instance.set_password(password)
        
        for attr, value in validate_data.items():
            setattr(instance,attr,value)
        instance.save()

        if subscribed_artists_data is not None:
            instance.subscribed_artists.set(subscribed_artists_data)
        if favorite_songs_data is not None:
            instance.favorite_songs.set(favorite_songs_data)
        
        return instance




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





