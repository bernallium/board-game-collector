from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('games/', views.games_index, name='index'),
    path('games/<int:game_id>/', views.games_detail, name='detail'),
    path('games/create/', views.GameCreate.as_view(), name='games_create'), # Need to call as_view() so that te GameCreate class is returned as a view function
    path('games/<int:pk>/update/', views.GameUpdate.as_view(), name='games_update'),
    path('games/<int:pk>/delete/', views.GameDelete.as_view(), name='games_delete'),
    path('games/<int:game_id>/add_session/', views.add_session, name='add_session'),
    path('games/<int:game_id>/add_photo/', views.add_photo, name='add_photo'),

    path('labels/', views.LabelList.as_view(), name='labels'),
    path('labels/<int:pk>/', views.LabelDetail.as_view(), name='labels_detail'),
    path('labels/create/', views.LabelCreate.as_view(), name='labels_create'),
    path('labels/<int:pk>/update/', views.LabelUpdate.as_view(), name='labels_update'),
    path('labels/<int:pk>/delete/', views.LabelDelete.as_view(), name='labels_delete'),

    path('accounts/signup/', views.signup, name='signup'),
]