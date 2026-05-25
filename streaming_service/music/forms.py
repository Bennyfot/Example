from django import forms
from .models import Track


class LoginForm(forms.Form):
    username = forms.CharField(label='Логин', max_length=150)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    username = forms.CharField(label='Логин', max_length=150)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('password') != cleaned.get('password2'):
            raise forms.ValidationError('Пароли не совпадают')
        return cleaned


class ArtistForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=200)
    bio = forms.CharField(label='Биография', required=False,
                          widget=forms.Textarea(attrs={'rows': 3}))


class ArtistFilterForm(forms.Form):
    name = forms.CharField(label='Поиск по имени', required=False)
    genre_id = forms.IntegerField(label='Жанр', required=False,
                                  widget=forms.Select)


class AlbumFilterForm(forms.Form):
    title = forms.CharField(label='Поиск по названию', required=False)
    year_from = forms.IntegerField(label='Год от', required=False)


class PlaylistForm(forms.Form):
    name = forms.CharField(label='Название плейлиста', max_length=200)
    tracks = forms.ModelMultipleChoiceField(
        queryset=Track.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Треки'
    )