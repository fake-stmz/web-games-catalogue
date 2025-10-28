from django.shortcuts import render, redirect
from .models import Game, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    
    games = Game.objects.prefetch_related('categories').all()
    categories = Category.objects.all()
    years = Game.objects.values_list('release_year', flat=True).distinct().order_by('release_year')
    
    search_query = request.GET.get('search', '')
    if search_query:
        games = games.filter(name__icontains=search_query)

    category_filter = request.GET.get('category', '')
    if category_filter:
        games = games.filter(categories__id=category_filter)

    year_filter = request.GET.get('year', '')
    if year_filter:
        games = games.filter(release_year=year_filter)

    return render(request, 'index.html', {'games': games, 'categories': categories, 'years': years})

def profile(request):
    return render(request, 'profile.html')

def register_page(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'register.html', {'error': 'Пароли не совпадают.'})
        
    return render(request, 'register.html')

def login_page(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'error': 'Неверное имя пользователя или пароль.'})

    return render(request, 'login.html')

def logout_page(request):
    
    logout(request)
    
    return redirect('index')