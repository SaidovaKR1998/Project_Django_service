from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Client, Message, Mailing, MailingLog


# Главная страница
def index(request):
    total_mailings = Mailing.objects.all().count()
    active_mailings = Mailing.objects.filter(status='started').count()
    unique_clients = Client.objects.distinct().count()

    context = {
        'total_mailings': total_mailings,
        'active_mailings': active_mailings,
        'unique_clients': unique_clients,
    }
    return render(request, 'service/index.html', context)


# Клиенты
@login_required
def client_list(request):
    clients = Client.objects.filter(owner=request.user)
    return render(request, 'service/client_list.html', {'clients': clients})


@login_required
def client_create(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        full_name = request.POST.get('full_name')
        comment = request.POST.get('comment')

        client = Client.objects.create(
            email=email,
            full_name=full_name,
            comment=comment,
            owner=request.user
        )
        messages.success(request, 'Клиент успешно создан!')
        return redirect('service:client_list')

    return render(request, 'service/client_form.html')


# Сообщения
@login_required
def message_list(request):
    messages_list = Message.objects.filter(owner=request.user)
    return render(request, 'service/message_list.html', {'messages': messages_list})


@login_required
def message_create(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        body = request.POST.get('body')

        message = Message.objects.create(
            subject=subject,
            body=body,
            owner=request.user
        )
        messages.success(request, 'Сообщение успешно создано!')
        return redirect('service:message_list')

    return render(request, 'service/message_form.html')


# Рассылки
@login_required
def mailing_list(request):
    mailings = Mailing.objects.filter(owner=request.user)
    return render(request, 'service/mailing_list.html', {'mailings': mailings})


@login_required
def mailing_create(request):
    if request.method == 'POST':
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        message_id = request.POST.get('message')
        client_ids = request.POST.getlist('clients')

        message = Message.objects.get(id=message_id, owner=request.user)
        mailing = Mailing.objects.create(
            start_time=start_time,
            end_time=end_time,
            status='created',
            message=message,
            owner=request.user
        )
        mailing.clients.set(Client.objects.filter(id__in=client_ids, owner=request.user))

        messages.success(request, 'Рассылка успешно создана!')
        return redirect('service:mailing_list')

    messages_list = Message.objects.filter(owner=request.user)
    clients_list = Client.objects.filter(owner=request.user)
    return render(request, 'service/mailing_form.html', {
        'messages': messages_list,
        'clients': clients_list
    })


# Статистика
@login_required
def statistics(request):
    user_mailings = Mailing.objects.filter(owner=request.user)

    total_mailings = user_mailings.count()
    active_mailings = user_mailings.filter(status='started').count()

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