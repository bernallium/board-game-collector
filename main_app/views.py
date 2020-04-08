from django.shortcuts import render, redirect
from .models import Game
from .forms import SessionForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# class Game: 
#     def __init__(self, name, category, rating, age, min_players, max_players, description):
#         self.name = name
#         self.category = category
#         self.rating = rating
#         self.age = age
#         self.min_players = min_players
#         self.max_players = max_players
#         self.description = description

# games = [
#     Game('Catan', 'Strategy', 8.5, 10, 3, 4, 
#     'In Catan, players try to be the dominant force on the island of Catan by building settlements, cities, and roads. On each turn dice are rolled to determine what resources the island produces. Players collect these resources (cards)—wood, grain, brick, sheep, or stone—to build up their civilizations to get to 10 victory points and win the game.'),
#     Game('Saboteur', 'Party', 7.2, 8, 3, 10, 
#     'Players take on the role of dwarves. As miners, they are in a mine, hunting for gold. Suddenly, a pick axe swings down and shatters the mine lamp. The saboteur has struck. But which of the players are saboteurs? Will you find the gold, or will the fiendish actions of the saboteurs lead them to it first? After three rounds, the player with the most gold is the winner.'),
#     Game('The Resistance', 'Party', 9, 13, 5, 10,
#     'The Resistance is a party game of social deduction. It is designed for five to ten players, lasts about 30 minutes, and has no player elimination. The Resistance is inspired by Mafia/Werewolf, yet it is unique in its core mechanics, which increase the resources for informed decisions, intensify player interaction, and eliminate player elimination.'),
# ]

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def games_index(request):
    games = Game.objects.all() # Get all the games
    return render(request, 'games/index.html', { 'games': games })

# def games_detail(request, game_id):
#     game = Game.objects.get(id=game_id)
#     return render(request, 'games/detail.html', { 'game': game })

def games_detail(request, game_id):
    game = Game.objects.get(id=game_id)
    session_form = SessionForm()
    return render(request, 'games/detail.html', {
        'game': game, 'session_form': session_form, # Include the game and session_form in the context
        })

def add_session(request, game_id):
    # Create the ModelForm using the data in request.POST
    form = SessionForm(request.POST)
    # Validate the form
    if form.is_valid():
        # Don't save the form to the db until it has the game_id assigned
        new_session = form.save(commit=False)
        new_session.game_id = game_id
        new_session.save()
    return redirect('detail', game_id=game_id) # Always be sure to redirect instead of render if data has been changed in the database.

class GameCreate(CreateView):
    model = Game
    fields = '__all__' # Alternatively: fields = ['name', 'breed', 'description', 'age']
    success_url = '/games/' # Redirect URL

class GameUpdate(UpdateView):
    model = Game
    fields = ['rating', 'category', 'description']

class GameDelete(DeleteView):
    model = Game
    success_url = '/games/'