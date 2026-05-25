from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('', views.artist_list, name='artist_list'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Artists
    path('artists/', views.artist_list, name='artist_list'),
    path('artists/create/', views.artist_create, name='artist_create'),
    path('artists/<int:artist_id>/', views.artist_detail, name='artist_detail'),

    # Albums
    path('albums/', views.album_list, name='album_list'),
    path('albums/<int:album_id>/', views.album_detail, name='album_detail'),

    # Playlists
    path('playlists/', views.playlist_list, name='playlist_list'),
    path('playlists/create/', views.playlist_create, name='playlist_create'),
    path('playlists/<int:playlist_id>/', views.playlist_detail, name='playlist_detail'),
    path('playlists/<int:playlist_id>/edit/', views.playlist_edit, name='playlist_edit'),
    path('playlists/<int:playlist_id>/delete/', views.playlist_delete, name='playlist_delete'),
]