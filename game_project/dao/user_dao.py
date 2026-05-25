from typing import List, Optional
from apps.users.models import CustomUser
from dto.user_dto import UserDTO, UserLeaderboardDTO, UserCreateDTO, UserUpdateDTO

class UserDAO:
    @staticmethod
    def get_all_users() -> List[UserDTO]:
        """Возвращает список всех пользователей в виде DTO"""
        users = CustomUser.objects.all()
        return [
            UserDTO(
                id=user.id,
                username=user.username,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                rating=user.rating,
                games_played=user.games_played
            )
            for user in users
        ]
    
    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[UserDTO]:
        """Возвращает пользователя по ID в виде DTO"""
        try:
            user = CustomUser.objects.get(id=user_id)
            return UserDTO(
                id=user.id,
                username=user.username,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                rating=user.rating,
                games_played=user.games_played
            )
        except CustomUser.DoesNotExist:
            return None
    
    @staticmethod
    def get_user_model(user_id: int) -> Optional[CustomUser]:
        """Возвращает модель пользователя (для операций, требующих сохранения)"""
        try:
            return CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return None
    
    @staticmethod
    def update_rating(user_id: int, new_rating: int) -> Optional[UserDTO]:
        """Обновляет рейтинг и возвращает обновленного пользователя в виде DTO"""
        user = CustomUser.objects.get(id=user_id)
        user.rating = new_rating
        user.save()
        return UserDAO.get_user_by_id(user_id)
    
    @staticmethod
    def increment_games_played(user_id: int) -> Optional[UserDTO]:
        """Увеличивает счетчик игр и возвращает обновленного пользователя"""
        user = CustomUser.objects.get(id=user_id)
        user.games_played += 1
        user.save()
        return UserDAO.get_user_by_id(user_id)
    
    @staticmethod
    def filter_by_min_rating(min_rating: int) -> List[UserLeaderboardDTO]:
        """Фильтрует пользователей по минимальному рейтингу и возвращает DTO для таблицы лидеров"""
        users = CustomUser.objects.filter(rating__gte=min_rating).order_by('-rating')
        result = []
        for position, user in enumerate(users, start=1):
            result.append(UserLeaderboardDTO(
                id=user.id,
                username=user.username,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                rating=user.rating,
                games_played=user.games_played,
                position=position
            ))
        return result
    
    @staticmethod
    def create_user(create_dto: UserCreateDTO) -> UserDTO:
        """Создает пользователя из DTO"""
        from django.contrib.auth.hashers import make_password
        user = CustomUser.objects.create(
            username=create_dto.username,
            email=create_dto.email,
            first_name=create_dto.first_name,
            last_name=create_dto.last_name,
            password=make_password(create_dto.password)
        )
        return UserDAO.get_user_by_id(user.id)
    
    @staticmethod
    def update_user(update_dto: UserUpdateDTO) -> Optional[UserDTO]:
        """Обновляет пользователя из DTO"""
        user = CustomUser.objects.get(id=update_dto.user_id)
        if update_dto.rating is not None:
            user.rating = update_dto.rating
        if update_dto.games_played is not None:
            user.games_played = update_dto.games_played
        if update_dto.first_name is not None:
            user.first_name = update_dto.first_name
        if update_dto.last_name is not None:
            user.last_name = update_dto.last_name
        if update_dto.email is not None:
            user.email = update_dto.email
        user.save()
        return UserDAO.get_user_by_id(user.id)