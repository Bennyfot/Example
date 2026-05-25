from typing import Optional, List
from django.db.models import QuerySet
from .models import Artist, Album, Track, Genre, Playlist


class ArtistDAO:
    """DAO для работы с исполнителями."""

    @staticmethod
    def get_all() -> QuerySet:
        return Artist.objects.all()

    @staticmethod
    def get_by_id(artist_id: int) -> Optional[Artist]:
        try:
            return Artist.objects.get(id=artist_id)
        except Artist.DoesNotExist:
            return None

    @staticmethod
    def filter(name: str = "", genre_id: Optional[int] = None) -> QuerySet:
        """Фильтрация исполнителей по имени и жанру."""
        qs = Artist.objects.all()
        if name:
            qs = qs.filter(name__icontains=name)
        if genre_id:
            qs = qs.filter(genres__id=genre_id)
        return qs.distinct()

    @staticmethod
    def create(name: str, bio: str, genre_ids: List[int]) -> Artist:
        artist = Artist.objects.create(name=name, bio=bio)
        if genre_ids:
            artist.genres.set(genre_ids)
        return artist


class AlbumDAO:
    @staticmethod
    def get_by_id(album_id: int) -> Optional[Album]:
        try:
            return Album.objects.get(id=album_id)
        except Album.DoesNotExist:
            return None

    @staticmethod
    def filter(title: str = "", artist_id: Optional[int] = None,
               year_from: Optional[int] = None) -> QuerySet:
        qs = Album.objects.select_related('artist').all()
        if title:
            qs = qs.filter(title__icontains=title)
        if artist_id:
            qs = qs.filter(artist_id=artist_id)
        if year_from:
            qs = qs.filter(release_year__gte=year_from)
        return qs


class TrackDAO:
    @staticmethod
    def get_by_id(track_id: int) -> Optional[Track]:
        try:
            return Track.objects.get(id=track_id)
        except Track.DoesNotExist:
            return None

    @staticmethod
    def get_by_album(album_id: int) -> QuerySet:
        return Track.objects.filter(album_id=album_id)


class GenreDAO:
    @staticmethod
    def get_all() -> QuerySet:
        return Genre.objects.all()

    @staticmethod
    def get_by_id(genre_id: int) -> Optional[Genre]:
        try:
            return Genre.objects.get(id=genre_id)
        except Genre.DoesNotExist:
            return None


class PlaylistDAO:
    @staticmethod
    def get_by_id(playlist_id: int) -> Optional[Playlist]:
        try:
            return Playlist.objects.get(id=playlist_id)
        except Playlist.DoesNotExist:
            return None

    @staticmethod
    def get_by_owner(user) -> QuerySet:
        return Playlist.objects.filter(owner=user)

    @staticmethod
    def create(name: str, owner, track_ids: List[int]) -> Playlist:
        playlist = Playlist.objects.create(name=name, owner=owner)
        if track_ids:
            playlist.tracks.set(track_ids)
        return playlist

    @staticmethod
    def update(playlist: Playlist, name: str, track_ids: List[int]) -> Playlist:
        playlist.name = name
        playlist.save()
        playlist.tracks.set(track_ids)
        return playlist

    @staticmethod
    def delete(playlist: Playlist) -> None:
        playlist.delete()