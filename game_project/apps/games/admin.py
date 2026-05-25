from django.contrib import admin
from .models import Game, PlayerGameRecord

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'max_score')
    search_fields = ('name',)

@admin.register(PlayerGameRecord)
class PlayerGameRecordAdmin(admin.ModelAdmin):
    list_display = ('player', 'game', 'score', 'played_at')
    list_filter = ('game', 'played_at')
    search_fields = ('player__username', 'game__name')