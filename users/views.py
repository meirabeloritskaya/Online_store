from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Сохраняем нового пользователя
            login(request, user)  # Автоматически авторизуем после регистрации

            # Отправляем приветственное письмо
            send_mail(
                'Добро пожаловать на сайт!',
                'Спасибо за регистрацию!',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            return redirect(settings.REGISTER_REDIRECT_URL)  # Перенаправление на главную страницу
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html', {'form': form})


class CustomLoginView(LoginView):

    template_name = 'users/login.html'
    redirect_authenticated_user = True  # Перенаправление, если пользователь уже авторизован
    success_url = settings.LOGIN_REDIRECT_URL  # Перенаправление после успешной авторизации


class CustomLogoutView(LogoutView):
    template_name = ''