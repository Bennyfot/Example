from django.db import models
from apps.games.models import Game
from apps.users.models import CustomUser

class Achievement(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='achievements', verbose_name='Игра')
    required_score = models.IntegerField(verbose_name='Необходимый балл')
    description = models.TextField(blank=True, verbose_name='Описание')
    
    def __str__(self):
        return f"{self.name} ({self.game.name})"
    
    class Meta:
        verbose_name = 'Достижение'
        verbose_name_plural = 'Достижения'

class UserAchievement(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.achievement.name}"
    
    class Meta:
        unique_together = ('user', 'achievement')
        verbose_name = 'Достижение пользователя'
        verbose_name_plural = 'Достижения пользователей'