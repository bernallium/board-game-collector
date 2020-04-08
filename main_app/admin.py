from django.contrib import admin

# Import your models
from .models import Game
from .models import Session

# Register your models
admin.site.register(Game)
admin.site.register(Session)