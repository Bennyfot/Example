from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):
    """Жанр музыки (Rock, Pop, Jazz и т.д.). Связь M:M с Artist."""
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Artist(models.Model):
    """Исполнитель. Имеет M:M с Genre и 1:M с Album."""
    name = models.CharField(max_length=200, verbose_name='Имя')
    bio = models.TextField(blank=True, verbose_name='Биография')
    genres = models.ManyToManyField(Genre, blank=True, related_name='artists',
                                    verbose_name='Жанры')

    class Meta:
        verbose_name = 'Исполнитель'
        verbose_name_plural = 'Исполнители'

    def __str__(self):
        return self.name


class Album(models.Model):
    """Альбом. Принадлежит одному Artist (1:M), содержит много Track."""
    title = models.CharField(max_length=200, verbose_name='Название')
    release_year = models.IntegerField(verbose_name='Год выпуска')
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE,
                               related_name='albums', verbose_name='Исполнитель')

    class Meta:
        verbose_name = 'Альбом'
        verbose_name_plural = 'Альбомы'

    def __str__(self):
        return f"{self.title} ({self.artist.name})"


class Track(models.Model):
    """Трек. Принадлежит одному Album (1:M). Может быть во многих Playlist."""
    title = models.CharField(max_length=200, verbose_name='Название')
    duration_seconds = models.IntegerField(verbose_name='Длительность (сек)')
    album = models.ForeignKey(Album, on_delete=models.CASCADE,
                              related_name='tracks', verbose_name='Альбом')

    class Meta:
        verbose_name = 'Трек'
        verbose_name_plural = 'Треки'

    def __str__(self):
        return f"{self.title} — {self.album.title}"


class Playlist(models.Model):
    """Плейлист пользователя. Владелец — User (1:M), треки — M:M."""
    name = models.CharField(max_length=200, verbose_name='Название')
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='playlists', verbose_name='Владелец')
    tracks = models.ManyToManyField(Track, blank=True, related_name='playlists',
                                    verbose_name='Треки')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')

    class Meta:
        verbose_name = 'Плейлист'
        verbose_name_plural = 'Плейлисты'

    def __str__(self):
        return f"{self.name} ({self.owner.username})"