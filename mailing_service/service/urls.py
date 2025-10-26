from django.urls import path
from . import views

app_name = 'service'

urlpatterns = [
    path('', views.index, name='home'),
    path('statistics/', views.statistics, name='statistics'),

    # Клиенты
    path('clients/', views.client_list, name='client_list'),
    path('clients/create/', views.client_create, name='client_create'),

    # Сообщения
    path('messages/', views.message_list, name='message_list'),
    path('messages/create/', views.message_create, name='message_create'),

    # Рассылки
    path('mailings/', views.mailing_list, name='mailing_list'),
    path('mailings/create/', views.mailing_create, name='mailing_create'),
]