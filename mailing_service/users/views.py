from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import secrets

from .forms import UserRegisterForm, UserLoginForm
from .models import User


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email_verified = False  # Email не подтвержден
            user.save()

            # В реальном приложении здесь был бы код отправки подтверждающего письма
            # Для примера просто авторизуем пользователя
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались!')
            return redirect('service:home')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('service:home')
    else:
        form = UserLoginForm()

    return render(request, 'users/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы.')
    return redirect('service:home')


@login_required
def profile(request):
    return render(request, 'users/profile.html')