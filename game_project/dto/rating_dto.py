"""DTO для рейтинга"""
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class RatingDTO:
    """DTO рейтинга пользователя"""
    user_id: int
    username: str
    rating: int
    games_played: int
    position: int
    
@dataclass
class RatingRecalculationDTO:
    """DTO для пересчета рейтинга"""
    user_id: int
    old_rating: int
    new_rating: int
    delta: int
    games_count: int
    total_score: int

@dataclass
class LeaderboardFilterDTO:
    """DTO для фильтрации таблицы лидеров"""
    min_rating: int = 0
    limit: int = 50