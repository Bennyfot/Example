# admin.py — регистрация моделей в админке для удобства наполнения данными
from django.contrib import admin
from .models import Artist, Album, Track, Genre, Playlist

admin.site.register(Artist)
admin.site.register(Album)
admin.site.register(Track)
admin.site.register(Genre)
admin.site.register(Playlist)