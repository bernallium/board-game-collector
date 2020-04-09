from django.contrib import admin

# Import your models
from .models import Game, Session, Photo

# Register your models
admin.site.register(Game)
admin.site.register(Session)
admin.site.register(Photo)