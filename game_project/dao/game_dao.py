from apps.games.models import Game, PlayerGameRecord

class GameDAO:
    @staticmethod
    def get_all_games():
        return Game.objects.all()
    
    @staticmethod
    def get_game_by_id(game_id):
        try:
            return Game.objects.get(id=game_id)
        except Game.DoesNotExist:
            return None
    
    @staticmethod
    def filter_games_by_name(name_filter):
        if name_filter:
            return Game.objects.filter(name__icontains=name_filter)
        return Game.objects.all()
    
    @staticmethod
    def get_player_records_for_game(game_id):
        return PlayerGameRecord.objects.filter(game_id=game_id).order_by('-score')
    
    @staticmethod
    def get_game_with_achievements(game_id):
        from apps.ratings.models import Achievement
        game = GameDAO.get_game_by_id(game_id)
        if game:
            achievements = Achievement.objects.filter(game=game)
            return game, achievements
        return None, []