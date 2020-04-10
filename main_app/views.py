from django.shortcuts import render, redirect
from .models import Game, Label, Photo
from .forms import SessionForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView

import uuid
import boto3

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

S3_BASE_URL = 'https://s3.us-east-2.amazonaws.com/'
BUCKET= 'bgamecollector'

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

# def games_index(request):
#     games = Game.objects.all() # Get all the games (does not consider which user's games)
#     return render(request, 'games/index.html', { 'games': games })

def games_index(request):
    games = Game.objects.filter(user=request.user)
    # You could also retrieve the logged in user's games like this
    # games = request.user.game_set.all()
    return render(request, 'games/index.html', { 'games': games })

# def games_detail(request, game_id):
#     game = Game.objects.get(id=game_id)
#     return render(request, 'games/detail.html', { 'game': game })

@login_required
def games_detail(request, game_id):
    game = Game.objects.get(id=game_id)
    session_form = SessionForm()
    return render(request, 'games/detail.html', {
        'game': game, 'session_form': session_form, # Include the game and session_form in the context
        })

@login_required
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

@login_required
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

class GameCreate(LoginRequiredMixin, CreateView): # GameCreate inherits from CreateView
    model = Game
    # fields = '__all__' # Need to not include user
    fields = ['name', 'rating', 'category', 'age', 'min_players', 'max_players', 'description']
    success_url = '/games/' # Redirect URL

    # form_valid is an inherited method from CreateView called when a valid game form is being submitted
    def form_valid(self, form):
        # Assign the logged in user (self.request.user)
        form.instance.user = self.request.user  # Assign the currently logged in user to the current game instance (form.instance is the game)
        # NOTE: the game instance has not been saved to the database yet
        # Let the CreateView do its job as usual so that the form is saved upon validation
        return super().form_valid(form)

class GameUpdate(LoginRequiredMixin, UpdateView):
    model = Game
    fields = ['rating', 'category', 'description']
    # TODO: Need rediect here?

class GameDelete(LoginRequiredMixin, DeleteView):
    model = Game
    success_url = '/games/'

def signup(request):
    error_message = ''
    if request.method == 'POST':
        # This is how to create a 'user' form object that includes the data from the browser
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() # Add the user to the database
            login(request, user) # Log a user in via code
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

class LabelList(ListView):
    model = Label

class LabelDetail(DetailView):
    model = Label

class LabelCreate(CreateView):
    model = Label
    fields = '__all__'

class LabelUpdate(UpdateView):
    model = Label
    fields = ['name']

class LabelDelete(DeleteView):
    model = Label
    success_url = '/toys/'
