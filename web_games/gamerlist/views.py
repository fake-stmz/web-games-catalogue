from django.shortcuts import render, redirect
from .models import Game, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


def index(request):
    """Список игр"""

    # Получение всех игр, категорий и годов выпуска
    games = Game.objects.prefetch_related('categories').all()
    categories = Category.objects.all()
    years = (Game.objects.values_list('release_year', flat=True)
             .distinct().order_by('release_year'))

    # Фильтры и поиск

    # Поиск
    search_query = request.GET.get('search', '')
    if search_query:
        games = games.filter(name__icontains=search_query)

    # Фильтр по категории
    category_filter = request.GET.get('category', '')
    if category_filter:
        games = games.filter(categories__id=category_filter)

    # Фильтр по году выпуска
    year_filter = request.GET.get('year', '')
    if year_filter:
        games = games.filter(release_year=year_filter)

    # Контекст для передачи в шаблон
    context = {
        'games': games,
        'categories': categories,
        'years': years
    }

    return render(request, 'index.html', context)


def profile(request):
    """Страница профиля пользователя"""

    return render(request, 'profile.html')


def register_page(request):
    """Страница регистрации"""

    if request.method == 'POST':
        # Получение введенных данных
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Подтверждение пароля
        if password == confirm_password:
            # Регистрация и вход
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            login(request, user)
            return redirect('index')
        else:
            # Вывод ошибки
            return render(request, 'register.html',
                          {'error': 'Пароли не совпадают.'})

    return render(request, 'register.html')


def login_page(request):
    """Страница входа"""

    if request.method == 'POST':
        # Получение введенных данных
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Попытка аутентификации
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Вход и переход к списку игр
            login(request, user)
            return redirect('index')
        else:
            # Вывод ошибки
            return render(request, 'login.html',
                          {'error': 'Неверное имя пользователя или пароль.'})

    return render(request, 'login.html')


def logout_page(request):
    """Выход из аккаунта"""

    logout(request)

    return redirect('index')
