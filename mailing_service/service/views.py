from django.shortcuts import render
from .models import Mailing, Client

def index(request):
    # Считаем статистику
    total_mailings = Mailing.objects.all().count()
    active_mailings = Mailing.objects.filter(status='started').count()
    unique_clients = Client.objects.distinct().count()

    context = {
        'total_mailings': total_mailings,
        'active_mailings': active_mailings,
        'unique_clients': unique_clients,
    }
    return render(request, 'service/index.html', context)
