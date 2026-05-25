from typing import Optional, List
from django.contrib.auth.models import User
from . import dao
from .dto import ArtistDTO, PlaylistDTO, FilterDTO, ValidationError


class ArtistService:
    """Сервис для работы с исполнителями."""

    @staticmethod
    def list_artists(filter_dto: FilterDTO):
        """Возвращает отфильтрованный список исполнителей."""
        return dao.ArtistDAO.filter(
            name=filter_dto.name,
            genre_id=filter_dto.genre_id
        )

    @staticmethod
    def get_artist(artist_id: int):
        return dao.ArtistDAO.get_by_id(artist_id)

    @staticmethod
    def create_artist(dto: ArtistDTO):
        """Создаёт исполнителя после валидации DTO."""
        dto.validate()
        return dao.ArtistDAO.create(
            name=dto.name,
            bio=dto.bio,
            genre_ids=dto.genre_ids or []
        )


class AlbumService:
    @staticmethod
    def list_albums(filter_dto: FilterDTO):
        return dao.AlbumDAO.filter(
            title=filter_dto.title,
            artist_id=filter_dto.artist_id,
            year_from=filter_dto.year_from
        )

    @staticmethod
    def get_album(album_id: int):
        return dao.AlbumDAO.get_by_id(album_id)


class TrackService:
    @staticmethod
    def get_all():
        from .models import Track
        return Track.objects.all()

    @staticmethod
    def get_track(track_id: int):
        return dao.TrackDAO.get_by_id(track_id)


class PlaylistService:
    """Сервис плейлистов — с проверкой авторизации и прав."""

    @staticmethod
    def get_user_playlists(user: User):
        if not user.is_authenticated:
            return []
        return dao.PlaylistDAO.get_by_owner(user)

    @staticmethod
    def get_playlist(playlist_id: int, user: User):
        """Возвращает плейлист. Авторизация + авторизация (право владения)."""
        playlist = dao.PlaylistDAO.get_by_id(playlist_id)
        if not playlist:
            return None, "Плейлист не найден"
        # Просмотр доступен всем
        return playlist, None

    @staticmethod
    def create_playlist(user: User, dto: PlaylistDTO):
        """Создание плейлиста (только для авторизованных)."""
        if not user.is_authenticated:
            raise PermissionError("Требуется авторизация")
        dto.validate()
        return dao.PlaylistDAO.create(
            name=dto.name,
            owner=user,
            track_ids=dto.track_ids or []
        )

    @staticmethod
    def update_playlist(user: User, playlist_id: int, dto: PlaylistDTO):
        """Редактирование — только владелец (авторизация)."""
        playlist = dao.PlaylistDAO.get_by_id(playlist_id)
        if not playlist:
            raise ValueError("Плейлист не найден")
        if playlist.owner_id != user.id:
            raise PermissionError("Нет прав на редактирование")
        dto.validate()
        return dao.PlaylistDAO.update(playlist, dto.name, dto.track_ids or [])

    @staticmethod
    def delete_playlist(user: User, playlist_id: int):
        """Удаление — только владелец."""
        playlist = dao.PlaylistDAO.get_by_id(playlist_id)
        if not playlist:
            raise ValueError("Плейлист не найден")
        if playlist.owner_id != user.id:
            raise PermissionError("Нет прав на удаление")
        dao.PlaylistDAO.delete(playlist)