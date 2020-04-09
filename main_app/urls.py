from django.urls import path
from .views import home, about, games_index, games_detail, GameCreate, GameUpdate, GameDelete, add_session, add_photo

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('games/', games_index, name='index'),
    path('games/<int:game_id>/', games_detail, name='detail'),
    path('games/create/', GameCreate.as_view(), name='games_create'), # Need to call as_view() so that te GameCreate class is returned as a view function
    path('games/<int:pk>/update/', GameUpdate.as_view(), name='games_update'),
    path('games/<int:pk>/delete/', GameDelete.as_view(), name='games_delete'),
    path('games/<int:game_id>/add_session/', add_session, name='add_session'),
    path('games/<int:game_id>/add_photo/', add_photo, name='add_photo'),
]