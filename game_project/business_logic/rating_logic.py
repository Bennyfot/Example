from dao.user_dao import UserDAO
from dao.player_game_record_dao import PlayerGameRecordDAO
from dto.rating_dto import RatingRecalculationDTO
from dto.user_dto import UserDTO

class RatingLogic:
    @staticmethod
    def recalculate_user_rating(user_id: int) -> RatingRecalculationDTO:
        """Пересчитывает рейтинг и возвращает DTO с деталями"""
        # Получаем старого пользователя
        old_user = UserDAO.get_user_by_id(user_id)
        if not old_user:
            return None
        
        old_rating = old_user.rating
        
        # Получаем все записи игр
        records = PlayerGameRecordDAO.get_user_all_records(user_id)
        
        if not records:
            new_rating = 0
            games_count = 0
            total_score = 0
        else:
            total_score = sum(record.score for record in records)
            games_count = len(records)
            new_rating = total_score // games_count
        
        # Обновляем рейтинг
        UserDAO.update_rating(user_id, new_rating)
        
        return RatingRecalculationDTO(
            user_id=user_id,
            old_rating=old_rating,
            new_rating=new_rating,
            delta=new_rating - old_rating,
            games_count=games_count,
            total_score=total_score
        )
    
    @staticmethod
    def get_user_position(user_id: int) -> int:
        """Возвращает позицию пользователя в рейтинге"""
        users = UserDAO.filter_by_min_rating(0)
        for position, user in enumerate(users, start=1):
            if user.id == user_id:
                return position
        return None