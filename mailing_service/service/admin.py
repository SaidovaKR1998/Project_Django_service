from django.contrib import admin
from .models import Client, Message

# Регистрируем модель для отображения в админке
admin.site.register(Client)
admin.site.register(Message)