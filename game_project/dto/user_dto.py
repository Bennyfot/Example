"""DTO для пользователей"""
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class UserDTO:
    """Базовый DTO пользователя"""
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    rating: int
    games_played: int
    
    @property
    def full_name(self) -> str:
        """Полное имя"""
        return f"{self.first_name} {self.last_name}".strip()
    
    @property
    def display_name(self) -> str:
        """Отображаемое имя"""
        return self.full_name if self.full_name else self.username

@dataclass
class UserProfileDTO(UserDTO):
    """DTO для профиля пользователя (с дополнительной информацией)"""
    position: Optional[int] = None
    achievements_count: int = 0
    
@dataclass
class UserLeaderboardDTO(UserDTO):
    """DTO для таблицы лидеров"""
    position: int = 0
    
@dataclass
class UserCreateDTO:
    """DTO для создания пользователя"""
    username: str
    password: str
    email: str = ""
    first_name: str = ""
    last_name: str = ""

@dataclass
class UserUpdateDTO:
    """DTO для обновления пользователя"""
    user_id: int
    rating: Optional[int] = None
    games_played: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None