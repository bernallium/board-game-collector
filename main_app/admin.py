from django.contrib import admin

# Import your models
from .models import Game, Session, Label, Photo

# Register your models
admin.site.register(Game)
admin.site.register(Session)
admin.site.register(Label)
admin.site.register(Photo)