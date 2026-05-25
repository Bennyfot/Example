from apps.games.models import PlayerGameRecord

class PlayerGameRecordDAO:
    @staticmethod
    def create_or_update_record(player_id, game_id, score):
        record, created = PlayerGameRecord.objects.get_or_create(
            player_id=player_id,
            game_id=game_id,
            defaults={'score': score}
        )
        if not created and score > record.score:
            record.score = score
            record.save()
        return record
    
    @staticmethod
    def get_record(player_id, game_id):
        try:
            return PlayerGameRecord.objects.get(player_id=player_id, game_id=game_id)
        except PlayerGameRecord.DoesNotExist:
            return None
    
    @staticmethod
    def get_records_for_user(user_id):
        return PlayerGameRecord.objects.filter(player_id=user_id).select_related('game')
    
    @staticmethod
    def get_top_scores_for_game(game_id, limit=10):
        return PlayerGameRecord.objects.filter(game_id=game_id).order_by('-score')[:limit]
    
    @staticmethod
    def get_user_all_records(user_id):
        return PlayerGameRecord.objects.filter(player_id=user_id)