import uuid
from django.db import models
from django.contrib.auth.hashers import make_password, check_password

from django.conf import settings
class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # ✅ Хешированный пароль будет храниться здесь

    username = models.CharField(max_length=255, unique=True, blank=True, null=True, default=None)
    date_of_birth = models.DateField(null=True, blank=True)  # Дата рождения
    gender = models.CharField(
        max_length=20, 
        choices=[("Man", "Man"), ("Woman", "Woman"), ("Non-binary", "Non-binary")], 
        null=True, blank=True
    )

    def set_password(self, raw_password):
        """Хеширует пароль перед сохранением"""
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        """Проверяет пароль"""
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.email


class Artist(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True, default="")
    image = models.URLField(blank=True, null=True, default="")
    listeners = models.CharField(max_length=255, blank=True, null=True, default="0")  # <-- добавлен default
    link = models.URLField(blank=True, null=True, default="")

    def __str__(self):
        return self.name



class Album(models.Model):
    id = models.IntegerField(primary_key=True)  # ID числовой, как в JSON
    title = models.CharField(max_length=255)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    release_date = models.DateField()
    image = models.URLField(blank=True, null=True, default="")  

    def __str__(self):
        return self.title


class Song(models.Model):
    id = models.IntegerField(primary_key=True)  # ID числовой, как в JSON
    title = models.CharField(max_length=255)
    artist = models.ForeignKey("Artist", on_delete=models.CASCADE)
    album = models.ForeignKey("Album", on_delete=models.CASCADE)
    image = models.URLField(blank=True, null=True, default="")  
    music_file = models.FileField(upload_to='music/')  # Загружаем сюда музыку
    fullscreen_image = models.ImageField(upload_to='image/', blank=True, null=True)
    duration = models.CharField(max_length=10)
    plays = models.IntegerField()

    def get_music_file_url(self):
        """
        Возвращает полный URL к аудиофайлу.
        Используем встроенный атрибут .url, который автоматически 
        формирует URL при правильной настройке MEDIA_URL.
        """
        if self.music_file:
            try:
                return self.music_file.url
            except Exception as e:
                # Если по какой-то причине не получилось, формируем вручную
                return f"{settings.MEDIA_URL}{self.music_file.name}"
        return None

    def __str__(self):
        return self.title