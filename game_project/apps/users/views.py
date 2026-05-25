from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import CustomUser

from dao.user_dao import UserDAO
from dao.game_dao import GameDAO
from dao.player_game_record_dao import PlayerGameRecordDAO
from dao.achievement_dao import AchievementDAO
from business_logic.rating_logic import RatingLogic
from business_logic.achievement_logic import AchievementLogic

# ==================== ОСНОВНЫЕ ФУНКЦИИ ====================

def home(request):
    """Главная страница"""
    if request.user.is_authenticated:
        return redirect('profile')
    return render(request, 'home.html')

def register(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}! Регистрация успешна!')
            return redirect('profile')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'register.html', {'form': form})

def login_view(request):
    """Вход в систему"""
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {username}!')
                return redirect('profile')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    """Выход из системы"""
    logout(request)
    messages.info(request, 'Вы вышли из системы')
    return redirect('home')

# ==================== ПРОФИЛЬ И ПОЛЬЗОВАТЕЛИ ====================

@login_required
def profile(request):
    """Профиль пользователя"""
    user = request.user
    records = PlayerGameRecordDAO.get_records_for_user(user.id)
    achievements = AchievementDAO.get_user_achievements(user.id)
    position = RatingLogic.get_user_position(user.id)
    
    context = {
        'user': user,
        'records': records,
        'achievements': achievements,
        'position': position,
    }
    return render(request, 'profile.html', context)

@login_required
def leaderboard(request):
    """Таблица лидеров с фильтрацией"""
    min_rating = request.GET.get('min_rating', 0)
    try:
        min_rating = int(min_rating)
    except ValueError:
        min_rating = 0
    
    users = UserDAO.filter_by_min_rating(min_rating)
    
    context = {
        'users': users,
        'min_rating': min_rating,
    }
    return render(request, 'leaderboard.html', context)

# ==================== ИГРЫ ====================

@login_required
def games_list(request):
    """Список всех игр с фильтрацией"""
    name_filter = request.GET.get('name', '')
    games = GameDAO.filter_games_by_name(name_filter)
    
    context = {
        'games': games,
        'name_filter': name_filter,
    }
    return render(request, 'games_list.html', context)

@login_required
def submit_score(request, game_id):
    """Отправка результата игры"""
    game = GameDAO.get_game_by_id(game_id)
    if not game:
        messages.error(request, 'Игра не найдена')
        return redirect('games_list')
    
    if request.method == 'POST':
        try:
            score = int(request.POST.get('score', 0))
            if score < 0 or score > game.max_score:
                messages.error(request, f'Некорректный счет. Допустимо от 0 до {game.max_score}')
                return redirect('games_list')
            
            # Сохраняем результат
            record = PlayerGameRecordDAO.create_or_update_record(request.user.id, game_id, score)
            
            # Обновляем количество сыгранных игр
            UserDAO.increment_games_played(request.user.id)
            
            # Пересчитываем рейтинг
            new_rating = RatingLogic.recalculate_user_rating(request.user.id)
            
            # Проверяем достижения
            new_achievements = AchievementLogic.check_new_achievements(request.user.id, game_id, score)
            
            messages.success(request, f'Результат сохранен! Ваш счет: {score}')
            
            context = {
                'game': game,
                'score': score,
                'new_rating': new_rating,
                'achievements': new_achievements,
            }
            return render(request, 'score_submitted.html', context)
            
        except ValueError:
            messages.error(request, 'Некорректный ввод счета')
    
    return render(request, 'submit_score.html', {'game': game})

# ==================== ДОСТИЖЕНИЯ ====================

@login_required
def my_achievements(request):
    """Список достижений пользователя"""
    earned = AchievementLogic.get_user_earned_achievements(request.user.id)
    available = AchievementLogic.get_available_achievements(request.user.id)
    
    context = {
        'earned': earned,
        'available': available,
    }
    return render(request, 'my_achievements.html', context)

# ==================== АДМИН-ПАНЕЛЬ ====================

@login_required
def admin_panel(request):
    """Кастомная админ-панель (только для администраторов)"""
    if not request.user.is_staff:
        messages.error(request, 'У вас нет доступа к админ-панели')
        return redirect('home')
    
    from apps.games.models import Game, PlayerGameRecord
    from apps.ratings.models import Achievement
    
    # Собираем статистику
    total_users = CustomUser.objects.count()
    total_games = Game.objects.count()
    total_achievements = Achievement.objects.count()
    total_records = PlayerGameRecord.objects.count()
    
    # Получаем топ-5 игроков
    top_players = CustomUser.objects.all().order_by('-rating')[:5]
    
    # Получаем популярные игры
    popular_games = Game.objects.annotate(
        plays_count=models.Count('player_records')
    ).order_by('-plays_count')[:5]
    
    context = {
        'total_users': total_users,
        'total_games': total_games,
        'total_achievements': total_achievements,
        'total_records': total_records,
        'top_players': top_players,
        'popular_games': popular_games,
    }
    return render(request, 'admin_dashboard.html', context)