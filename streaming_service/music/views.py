from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from . import dao
from .dto import ArtistDTO, PlaylistDTO, FilterDTO, ValidationError
from .services import ArtistService, AlbumService, TrackService, PlaylistService
from .forms import (LoginForm, RegisterForm, ArtistForm, ArtistFilterForm,
                    AlbumFilterForm, PlaylistForm)


# ===== Аутентификация =====

def login_view(request):
    """Авторизация пользователя."""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                return redirect('artist_list')
            messages.error(request, 'Неверный логин или пароль')
    else:
        form = LoginForm()
    return render(request, 'music/login.html', {'form': form})


def register_view(request):
    """Регистрация нового пользователя."""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Пользователь уже существует')
            else:
                User.objects.create_user(
                    username=username,
                    password=form.cleaned_data['password']
                )
                messages.success(request, 'Регистрация успешна. Войдите.')
                return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'music/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


# ===== Исполнители =====

def artist_list(request):
    """Список исполнителей с фильтрацией (по имени и жанру)."""
    filter_form = ArtistFilterForm(request.GET or None)
    # Инициализируем choices для жанров
    filter_form.fields['genre_id'].widget.choices = [('', '---')] + [
        (g.id, g.name) for g in dao.GenreDAO.get_all()
    ]

    filter_dto = FilterDTO()
    if filter_form.is_valid():
        filter_dto.name = filter_form.cleaned_data.get('name') or ""
        filter_dto.genre_id = filter_form.cleaned_data.get('genre_id')

    artists = ArtistService.list_artists(filter_dto)
    return render(request, 'music/artist_list.html', {
        'artists': artists,
        'filter_form': filter_form,
    })


def artist_detail(request, artist_id):
    """Детальная страница исполнителя + его альбомы."""
    artist = ArtistService.get_artist(artist_id)
    if not artist:
        return render(request, 'music/artist_detail.html', {'artist': None})
    albums = dao.AlbumDAO.filter(artist_id=artist_id)
    return render(request, 'music/artist_detail.html', {
        'artist': artist,
        'albums': albums,
    })


@login_required
def artist_create(request):
    """Создание исполнителя — только для авторизованных."""
    if request.method == 'POST':
        form = ArtistForm(request.POST)
        if form.is_valid():
            try:
                dto = ArtistDTO(
                    name=form.cleaned_data['name'],
                    bio=form.cleaned_data.get('bio', ''),
                )
                ArtistService.create_artist(dto)
                messages.success(request, 'Исполнитель создан')
                return redirect('artist_list')
            except ValidationError as e:
                for field, err in e.errors.items():
                    form.add_error(field, err)
    else:
        form = ArtistForm()
    return render(request, 'music/artist_form.html', {'form': form})


# ===== Альбомы =====

def album_list(request):
    """Список альбомов с фильтрацией (по названию и году)."""
    filter_form = AlbumFilterForm(request.GET or None)
    filter_dto = FilterDTO()
    if filter_form.is_valid():
        filter_dto.title = filter_form.cleaned_data.get('title') or ""
        filter_dto.year_from = filter_form.cleaned_data.get('year_from')

    albums = AlbumService.list_albums(filter_dto)
    return render(request, 'music/album_list.html', {
        'albums': albums,
        'filter_form': filter_form,
    })


def album_detail(request, album_id):
    """Альбом + список треков."""
    album = AlbumService.get_album(album_id)
    if not album:
        return render(request, 'music/album_detail.html', {'album': None})
    tracks = dao.TrackDAO.get_by_album(album_id)
    return render(request, 'music/album_detail.html', {
        'album': album,
        'tracks': tracks,
    })


# ===== Плейлисты (с авторизацией и авторизацией) =====

@login_required
def playlist_list(request):
    """Список плейлистов текущего пользователя."""
    playlists = PlaylistService.get_user_playlists(request.user)
    return render(request, 'music/playlist_list.html', {'playlists': playlists})


def playlist_detail(request, playlist_id):
    """Просмотр плейлиста (доступен всем)."""
    playlist, err = PlaylistService.get_playlist(playlist_id, request.user)
    if not playlist:
        messages.error(request, err or 'Не найден')
        return redirect('playlist_list')
    return render(request, 'music/playlist_detail.html', {
        'playlist': playlist,
        'is_owner': request.user.is_authenticated and playlist.owner_id == request.user.id,
    })


@login_required
def playlist_create(request):
    """Создание плейлиста — только авторизованные."""
    if request.method == 'POST':
        form = PlaylistForm(request.POST)
        if form.is_valid():
            try:
                dto = PlaylistDTO(
                    name=form.cleaned_data['name'],
                    track_ids=[t.id for t in form.cleaned_data['tracks']],
                )
                PlaylistService.create_playlist(request.user, dto)
                messages.success(request, 'Плейлист создан')
                return redirect('playlist_list')
            except ValidationError as e:
                for field, err in e.errors.items():
                    form.add_error(field, err)
            except PermissionError as e:
                messages.error(request, str(e))
    else:
        form = PlaylistForm()
    return render(request, 'music/playlist_form.html', {'form': form, 'edit': False})


@login_required
def playlist_edit(request, playlist_id):
    """Редактирование — только владелец."""
    playlist = dao.PlaylistDAO.get_by_id(playlist_id)
    if not playlist:
        messages.error(request, 'Не найден')
        return redirect('playlist_list')
    if request.method == 'POST':
        form = PlaylistForm(request.POST)
        if form.is_valid():
            try:
                dto = PlaylistDTO(
                    name=form.cleaned_data['name'],
                    track_ids=[t.id for t in form.cleaned_data['tracks']],
                )
                PlaylistService.update_playlist(request.user, playlist_id, dto)
                messages.success(request, 'Плейлист обновлён')
                return redirect('playlist_detail', playlist_id=playlist_id)
            except ValidationError as e:
                for field, err in e.errors.items():
                    form.add_error(field, err)
            except PermissionError as e:
                messages.error(request, str(e))
    else:
        form = PlaylistForm(initial={
            'name': playlist.name,
            'tracks': playlist.tracks.all(),
        })
    return render(request, 'music/playlist_form.html', {
        'form': form, 'edit': True, 'playlist': playlist,
    })


@login_required
def playlist_delete(request, playlist_id):
    """Удаление — только владелец, только POST."""
    if request.method == 'POST':
        try:
            PlaylistService.delete_playlist(request.user, playlist_id)
            messages.success(request, 'Плейлист удалён')
        except PermissionError as e:
            messages.error(request, str(e))
        except ValueError as e:
            messages.error(request, str(e))
    return redirect('playlist_list')