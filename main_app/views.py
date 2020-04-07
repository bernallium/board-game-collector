from django.shortcuts import render

class Game: 
    def __init__(self, name, category, rating, age, min_players, max_players, description):
        self.name = name
        self.category = category
        self.rating = rating
        self.age = age
        self.min_players = min_players
        self.max_players = max_players
        self.description = description

games = [
    Game('Catan', 'Strategy', 8.5, 10, 3, 4, 
    'In Catan, players try to be the dominant force on the island of Catan by building settlements, cities, and roads. On each turn dice are rolled to determine what resources the island produces. Players collect these resources (cards)—wood, grain, brick, sheep, or stone—to build up their civilizations to get to 10 victory points and win the game.'),
    Game('Saboteur', 'Party', 7, 8, 3, 10, 
    'Players take on the role of dwarves. As miners, they are in a mine, hunting for gold. Suddenly, a pick axe swings down and shatters the mine lamp. The saboteur has struck. But which of the players are saboteurs? Will you find the gold, or will the fiendish actions of the saboteurs lead them to it first? After three rounds, the player with the most gold is the winner.'),
    Game('The Resistance', 'Party', 9, 13, 5, 10,
    'The Resistance is a party game of social deduction. It is designed for five to ten players, lasts about 30 minutes, and has no player elimination. The Resistance is inspired by Mafia/Werewolf, yet it is unique in its core mechanics, which increase the resources for informed decisions, intensify player interaction, and eliminate player elimination.'),
]

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def games_index(request):
    return render(request, 'games/index.html', { 'games': games })