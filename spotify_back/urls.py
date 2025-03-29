
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, AlbumViewSet, SongViewSet, ArtistViewSet, delete_artist_by_id, get_library
from .views import toggle_artist_subscription, toggle_favorite_song

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'artists', ArtistViewSet)
router.register(r'albums', AlbumViewSet)
router.register(r'songs', SongViewSet)


urlpatterns = [
    path('', include(router.urls)), 
    path('api/artists/delete/<int:artist_id>/', delete_artist_by_id, name='delete_artist_by_id'),
    path('users/login/', UserViewSet.as_view({'post': 'login'}), name='user-login'),
    path('users/<uuid:user_id>/toggle-artist/<int:artist_id>/', toggle_artist_subscription),
    path('users/<uuid:user_id>/toggle-song/<int:song_id>/', toggle_favorite_song),
    path('/api/users/<uuid:user_id>/library/', get_library),
    path('auth/login/', UserViewSet.as_view({'post': 'login'})),
]

