from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    rating = models.IntegerField(default=0)
    games_played = models.IntegerField(default=0)
    
    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'