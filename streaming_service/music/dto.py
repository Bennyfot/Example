from dataclasses import dataclass
from typing import List, Optional


class ValidationError(Exception):
    """Исключение при невалидных данных."""
    def __init__(self, errors: dict):
        self.errors = errors
        super().__init__(str(errors))


@dataclass
class ArtistDTO:
    """DTO для создания/редактирования исполнителя."""
    name: str
    bio: str = ""
    genre_ids: Optional[List[int]] = None

    def validate(self):
        errors = {}
        if not self.name or len(self.name.strip()) < 2:
            errors['name'] = 'Имя должно содержать минимум 2 символа'
        if len(self.name) > 200:
            errors['name'] = 'Имя слишком длинное'
        if errors:
            raise ValidationError(errors)
        return True


@dataclass
class PlaylistDTO:
    """DTO для создания/редактирования плейлиста."""
    name: str
    track_ids: Optional[List[int]] = None

    def validate(self):
        errors = {}
        if not self.name or len(self.name.strip()) < 2:
            errors['name'] = 'Название должно содержать минимум 2 символа'
        if len(self.name) > 200:
            errors['name'] = 'Название слишком длинное'
        if errors:
            raise ValidationError(errors)
        return True


@dataclass
class FilterDTO:
    """DTO для параметров фильтрации."""
    name: str = ""
    genre_id: Optional[int] = None
    title: str = ""
    artist_id: Optional[int] = None
    year_from: Optional[int] = None