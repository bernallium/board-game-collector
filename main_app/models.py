from django.db import models
from django.urls import reverse
    
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