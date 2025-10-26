from django.contrib import admin
from .models import Client # Импортируем нашу модель

# Регистрируем модель для отображения в админке
admin.site.register(Client)
