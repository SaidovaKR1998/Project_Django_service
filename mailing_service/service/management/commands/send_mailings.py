from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from service.models import Mailing, MailingLog, Client
from django.conf import settings


class Command(BaseCommand):
    help = 'Запускает рассылку писем для активных рассылок'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Принудительно отправить все рассылки со статусом "created" или "started"',
        )

    def handle(self, *args, **options):
        now = timezone.now()
        force_send = options['force']

        if force_send:
            # Принудительно отправляем все рассылки кроме завершенных
            mailings_to_send = Mailing.objects.filter(
                status__in=['created', 'started']
            )
            self.stdout.write(f"Принудительная отправка: найдено {mailings_to_send.count()} рассылок")
        else:
            # Обычная логика - только те, у которых время пришло
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

            # Получаем всех клиентов этой рассылки
            clients = mailing.clients.all()
            self.stdout.write(f"Отправка рассылки {mailing.id} для {clients.count()} клиентов")

            for client in clients:
                try:
                    # Пытаемся отправить письмо
                    send_mail(
                        subject=mailing.message.subject,
                        message=mailing.message.body,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[client.email],
                        fail_silently=False,
                    )
                    # Если отправка успешна, пишем лог
                    MailingLog.objects.create(
                        status='success',
                        server_response='200 OK',
                        mailing=mailing,
                    )
                    success_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f"✓ Письмо для {client.email} отправлено")
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
                        self.style.ERROR(f"✗ Ошибка для {client.email}: {str(e)}")
                    )

        # Выводим итоговую статистику
        self.stdout.write("=" * 50)
        if success_count > 0 or error_count > 0:
            self.stdout.write(self.style.SUCCESS(f"ИТОГИ ОТПРАВКИ:"))
            self.stdout.write(self.style.SUCCESS(f"Успешно отправлено: {success_count}"))
            self.stdout.write(self.style.ERROR(f"Ошибок отправки: {error_count}"))
        else:
            self.stdout.write(self.style.WARNING("Нет рассылок для отправки."))
            self.stdout.write(self.style.WARNING("Используйте --force для принудительной отправки"))
