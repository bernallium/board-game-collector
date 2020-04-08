from django.urls import path
from .views import home, about, games_index, games_detail

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('games/', games_index, name='index'),
    path('games/<int:game_id>/', games_detail, name='detail'),
]