from django.contrib import admin
from django.urls import path
from apps.users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin-panel/', user_views.admin_panel, name='admin_panel'),
    path('', user_views.home, name='home'),
    path('register/', user_views.register, name='register'),
    path('login/', user_views.login_view, name='login'),
    path('logout/', user_views.logout_view, name='logout'),
    path('profile/', user_views.profile, name='profile'),
    path('leaderboard/', user_views.leaderboard, name='leaderboard'),
    path('games/', user_views.games_list, name='games_list'),
    path('submit_score/<int:game_id>/', user_views.submit_score, name='submit_score'),
    path('my_achievements/', user_views.my_achievements, name='my_achievements'),
]