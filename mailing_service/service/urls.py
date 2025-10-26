from django.urls import path
from . import views

app_name = 'service'

urlpatterns = [
    path('', views.index, name='home'), # Главная страница будет по адресу http://127.0.0.1:8000/
    path('statistics/', views.statistics, name='statistics'),
]