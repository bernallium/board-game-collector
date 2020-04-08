from django.db import models
from django.urls import reverse

# The first item in each 2-tuple represents the value that will be stored in the database
# The second item represents the human-friendly "display" value
ENJOYMENT_LEVEL = (
    ('l', 'Low'),
    ('m', 'Medium'),
    ('h', 'High'),
)

class Game(models.Model):
    name = models.CharField(max_length=100)
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    category = models.CharField(max_length=100)
    age = models.PositiveIntegerField(null=True)
    min_players = models.PositiveIntegerField(null=True)
    max_players = models.PositiveIntegerField(null=True)
    description = models.TextField(max_length=800)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'game_id': self.id})

# Add new Feeding model below Cat model
class Session(models.Model):
    
    date = models.DateField('Date played') # The first optional positional argument overrides the label
    enjoyment = models.CharField(
        'Enjoyment level',
        max_length=1, # Use just a single character to represent the level of enjoyment (low, medium, high)
        choices=ENJOYMENT_LEVEL, 
        default=ENJOYMENT_LEVEL[0][1], # Default to medium level of enjoyment
        )
    winner = models.CharField(max_length=100)

    # 1:M relationship ("A game can have many sessions")
    game = models.ForeignKey(Game, on_delete=models.CASCADE) # Django autmatically renames the FK as game_id in the database

    def __str__(self):
        return f"The game played on {self.date} had a {self.get_enjoyment_display()} level of enjoyment"
