"""DTO для достижений"""
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class AchievementDTO:
    """Базовый DTO достижения"""
    id: int
    name: str
    description: str
    required_score: int
    game_id: int
    game_name: str

@dataclass
class UserAchievementDTO:
    """DTO достижения пользователя"""
    achievement_id: int
    achievement_name: str
    game_name: str
    earned_at: datetime
    required_score: int
    
    @property
    def earned_date(self) -> str:
        """Дата получения"""
        return self.earned_at.strftime("%d.%m.%Y")

@dataclass
class EarnedAchievementDTO:
    """DTO для новых полученных достижений"""
    achievement: AchievementDTO
    is_new: bool = True