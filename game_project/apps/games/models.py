from django.db import models
from apps.users.models import CustomUser

class Game(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    max_score = models.IntegerField(verbose_name='Максимальный балл')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'

class PlayerGameRecord(models.Model):
    player = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='game_records')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='player_records')
    score = models.IntegerField(default=0)
    played_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.player.username} - {self.game.name}: {self.score}"
    
    class Meta:
        unique_together = ('player', 'game')
        verbose_name = 'Запись игры'
        verbose_name_plural = 'Записи игр'
        ordering = ['-played_at']