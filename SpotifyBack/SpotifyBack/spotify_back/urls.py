# spotify_back/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, AlbumViewSet, SongViewSet, ArtistViewSet, delete_artist_by_id


router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'artists', ArtistViewSet)
router.register(r'albums', AlbumViewSet)
router.register(r'songs', SongViewSet)


urlpatterns = [
    path('api/', include(router.urls)), 
    path('api/artists/delete/<int:artist_id>/', delete_artist_by_id, name='delete_artist_by_id'),
    path('users/login/', UserViewSet.as_view({'post': 'login'}), name='user-login'),
]

