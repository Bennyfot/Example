"""DTO для игр"""
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class GameDTO:
    """Базовый DTO игры"""
    id: int
    name: str
    description: str
    max_score: int
    
@dataclass
class GameWithStatsDTO(GameDTO):
    """DTO игры со статистикой"""
    players_count: int = 0
    average_score: float = 0.0
    top_score: int = 0

@dataclass
class PlayerGameRecordDTO:
    """DTO записи игры пользователя"""
    id: int
    player_id: int
    player_name: str
    game_id: int
    game_name: str
    score: int
    played_at: datetime
    
    @property
    def formatted_date(self) -> str:
        """Отформатированная дата"""
        return self.played_at.strftime("%d.%m.%Y %H:%M")

@dataclass
class SubmitScoreDTO:
    """DTO для отправки результата"""
    player_id: int
    game_id: int
    score: int
    
@dataclass
class GameFilterDTO:
    """DTO для фильтрации игр"""
    name_contains: Optional[str] = None
    min_score: Optional[int] = None
    max_score: Optional[int] = None