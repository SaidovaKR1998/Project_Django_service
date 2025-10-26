from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from service.models import Mailing, MailingLog, Client
from django.conf import settings


class Command(BaseCommand):
    help = 'Запускает рассылку писем для активных рассылок'

    def handle(self, *args, **options):
        now = timezone.now()

        # Находим рассылки, которые нужно отправить:
        # - Статус "created" или "started"
        # - Время начала уже наступило
        # - Время окончания еще не прошло
        mailings_to_send = Mailing.objects.filter(
            status__in=['created', 'started'],
            start_time__lte=now,
            end_time__gte=now
        )

        success_count = 0
        error_count = 0

        for mailing in mailings_to_send:
            # Меняем статус рассылки на "Запущена", если она была "Создана"
            if mailing.status == 'created':
                mailing.status = 'started'
                mailing.save()

            # Получаем всех клиентов этой рассылки (уже привязаны через ManyToMany)
            clients = mailing.clients.all()

            for client in clients:
                try:
                    # Пытаемся отправить письмо
                    send_mail(
                        subject=mailing.message.subject,
                        message=mailing.message.body,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[client.email],
                        fail_silently=False,  # Если ошибка, будет исключение
                    )
                    # Если отправка успешна, пишем лог
                    MailingLog.objects.create(
                        status='success',
                        server_response='200 OK',
                        mailing=mailing,
                    )
                    success_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f"Письмо для {client.email} отправлено.")
                    )

                except Exception as e:
                    # Если ошибка, пишем лог с ошибкой
                    MailingLog.objects.create(
                        status='failed',
                        server_response=str(e),
                        mailing=mailing,
                    )
                    error_count += 1
                    self.stdout.write(
                        self.style.ERROR(f"Ошибка для {client.email}: {str(e)}")
                    )

        # Помечаем завершенные рассылки
        completed_mailings = Mailing.objects.filter(
            status='started',
            end_time__lt=now
        )
        completed_count = completed_mailings.count()
        completed_mailings.update(status='completed')

        # Выводим итоговую статистику
        self.stdout.write("=" * 50)
        self.stdout.write(self.style.SUCCESS(f"ИТОГИ ОТПРАВКИ:"))
        self.stdout.write(self.style.SUCCESS(f"Успешно отправлено: {success_count}"))
        self.stdout.write(self.style.ERROR(f"Ошибок отправки: {error_count}"))
        self.stdout.write(self.style.WARNING(f"Завершено рассылок: {completed_count}"))

        if success_count == 0 and error_count == 0:
            self.stdout.write(self.style.WARNING("Нет рассылок для отправки."))
