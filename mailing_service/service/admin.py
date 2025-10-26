from django.contrib import admin
from .models import Client, Message, Mailing, MailingLog

# Регистрируем модель для отображения в админке
admin.site.register(Client)
admin.site.register(Message)
admin.site.register(Mailing)
admin.site.register(MailingLog)