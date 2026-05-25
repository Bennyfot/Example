from apps.ratings.models import Achievement, UserAchievement

class AchievementDAO:
    @staticmethod
    def get_achievements_by_game(game_id):
        return Achievement.objects.filter(game_id=game_id)
    
    @staticmethod
    def get_all_achievements():
        return Achievement.objects.all().select_related('game')
    
    @staticmethod
    def get_user_achievements(user_id):
        return UserAchievement.objects.filter(user_id=user_id).select_related('achievement__game')
    
    @staticmethod
    def add_user_achievement(user_id, achievement_id):
        obj, created = UserAchievement.objects.get_or_create(
            user_id=user_id,
            achievement_id=achievement_id
        )
        return obj
    
    @staticmethod
    def check_user_has_achievement(user_id, achievement_id):
        return UserAchievement.objects.filter(user_id=user_id, achievement_id=achievement_id).exists()