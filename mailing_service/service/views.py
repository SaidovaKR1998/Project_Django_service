from django.contrib.auth.decorators import login_required
from .models import Mailing, MailingLog, Client

@cache_page(60 * 15)  # Кешируем на 15 минут
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

@login_required
@cache_page(60 * 5)  # Кешируем на 5 минут
def statistics(request):
    # Статистика только для текущего пользователя
    user_mailings = Mailing.objects.filter(owner=request.user)

    total_mailings = user_mailings.count()
    active_mailings = user_mailings.filter(status='started').count()

    # Получаем логи для рассылок пользователя
    mailing_logs = MailingLog.objects.filter(mailing__owner=request.user)
    successful_attempts = mailing_logs.filter(status='success').count()
    failed_attempts = mailing_logs.filter(status='failed').count()
    total_attempts = mailing_logs.count()

    context = {
        'total_mailings': total_mailings,
        'active_mailings': active_mailings,
        'successful_attempts': successful_attempts,
        'failed_attempts': failed_attempts,
        'total_attempts': total_attempts,
    }
    return render(request, 'service/statistics.html', context)