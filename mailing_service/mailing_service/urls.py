from django.contrib import admin
from django.urls import path, include # Импортируем include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('service.urls')), # Подключаем URLs из приложения service
]