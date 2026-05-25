from dao.achievement_dao import AchievementDAO
from dao.player_game_record_dao import PlayerGameRecordDAO

class AchievementLogic:
    @staticmethod
    def check_new_achievements(user_id, game_id, score):
        achievements = AchievementDAO.get_achievements_by_game(game_id)
        new_achievements = []
        
        for achievement in achievements:
            if score >= achievement.required_score:
                if not AchievementDAO.check_user_has_achievement(user_id, achievement.id):
                    AchievementDAO.add_user_achievement(user_id, achievement.id)
                    new_achievements.append(achievement)
        
        return new_achievements
    
    @staticmethod
    def get_user_earned_achievements(user_id):
        return AchievementDAO.get_user_achievements(user_id)
    
    @staticmethod
    def get_available_achievements(user_id):
        all_achievements = AchievementDAO.get_all_achievements()
        user_achievements = AchievementDAO.get_user_achievements(user_id)
        user_achievement_ids = [ua.achievement.id for ua in user_achievements]
        
        available = []
        for ach in all_achievements:
            if ach.id not in user_achievement_ids:
                available.append(ach)
        
        return available