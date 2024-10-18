from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Электронная почта для авторизации
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)  # Аватар пользователя
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Номер телефона
    country = models.CharField(max_length=100, blank=True, null=True)  # Страна проживания

    # Указываем, что email будет использоваться для входа вместо username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Поля, которые требуются при создании пользователя через командную строку

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
    def __str__(self):
        return self.email
