from django.shortcuts import render, redirect
from .models import Game, Photo
from .forms import SessionForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView

import uuid
import boto3

S3_BASE_URL = 'https://s3.us-east-2.amazonaws.com/'
BUCKET= 'bgamecollector'

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

def add_photo(request, game_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # Need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):] # Create 6 random characters and then attach the file name without the file extension
        # Alternatively could make your key a path
        # This creates uniqe folder names with your photo inside
        # key = uuid.uuid4().hex[:6] + '/' + photo_file.name
        
        # Just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # Build the full url string (needs to be unique to avoid overwriting existing files)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # Can assign to game_id or game (if you have a game object)
            photo = Photo(url=url, game_id=game_id)
            photo.save()
        except Exception as e:
            print(e)
            print('An error occurred uploading file to S3')
    return redirect('detail', game_id=game_id)

class GameCreate(CreateView):
    model = Game
    fields = '__all__' # Alternatively: fields = ['name', 'breed', 'description', 'age']
    success_url = '/games/' # Redirect URL

class GameUpdate(UpdateView):
    model = Game
    fields = ['rating', 'category', 'description']
    # TODO: Need rediect here?

class GameDelete(DeleteView):
    model = Game
    success_url = '/games/'