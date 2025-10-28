from django.shortcuts import render
from .models import Game, Category

# Create your views here.
def index(request):
    games = Game.objects.prefetch_related('categories').all()
    categories = Category.objects.all()

    if request.method == 'GET' and 'search' in request.GET:
        search_query = request.GET.get('search', '')
        games = games.filter(name__icontains=search_query)

    if request.method == 'GET' and 'category' in request.GET:
        category_id = request.GET.get('category', '')
        games = games.filter(categories__id=category_id)

    return render(request, 'index.html', {'games': games, 'categories': categories})

def profile(request):
    pass

def register(request):
    pass

def login(request):
    pass

def logout(request):
    pass