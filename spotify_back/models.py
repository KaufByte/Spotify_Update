import uuid
from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=20,
        choices=[("Man", "Man"), ("Woman", "Woman"), ("Non-binary", "Non-binary")],
        null=True, blank=True
    )
    subscribed_artists = models.ManyToManyField('Artist', related_name='subscribers', blank=True)
    favorite_songs = models.ManyToManyField('Song', related_name='favorited_by', blank=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.email

class Artist(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    listeners = models.CharField(max_length=255, default="0")
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class Album(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    release_date = models.DateField()
    image = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

class Song(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    image = models.URLField(blank=True, null=True)
    music_file = models.FileField(upload_to='music/')
    fullscreen_image = models.ImageField(upload_to='image/', blank=True, null=True)
    duration = models.CharField(max_length=10)
    plays = models.IntegerField()

    def __str__(self):
        return self.title
