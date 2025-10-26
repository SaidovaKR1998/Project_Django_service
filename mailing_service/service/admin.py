from django.contrib import admin
from .models import Client, Message, Mailing, MailingLog


class ClientAdmin(admin.ModelAdmin):
    list_display = ['email', 'full_name', 'owner', 'comment']
    list_filter = ['owner']
    search_fields = ['email', 'full_name']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        if not obj.owner:
            obj.owner = request.user
        super().save_model(request, obj, form, change)


class MessageAdmin(admin.ModelAdmin):
    list_display = ['subject', 'body_preview', 'owner']
    list_filter = ['owner']
    search_fields = ['subject', 'body']

    def body_preview(self, obj):
        return obj.body[:50] + '...' if len(obj.body) > 50 else obj.body

    body_preview.short_description = 'Превью тела письма'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        if not obj.owner:
            obj.owner = request.user
        super().save_model(request, obj, form, change)


class MailingAdmin(admin.ModelAdmin):
    list_display = ['id', 'start_time', 'end_time', 'status', 'message', 'owner', 'clients_count']
    list_filter = ['status', 'owner', 'start_time']
    filter_horizontal = ['clients']

    def clients_count(self, obj):
        return obj.clients.count()

    clients_count.short_description = 'Кол-во клиентов'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        if not obj.owner:
            obj.owner = request.user
        super().save_model(request, obj, form, change)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "clients":
            # Показываем только клиентов текущего пользователя
            if not request.user.is_superuser:
                kwargs["queryset"] = Client.objects.filter(owner=request.user)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "message":
            # Показываем только сообщения текущего пользователя
            if not request.user.is_superuser:
                kwargs["queryset"] = Message.objects.filter(owner=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class MailingLogAdmin(admin.ModelAdmin):
    list_display = ['mailing', 'attempt_time', 'status', 'server_response_preview']
    list_filter = ['status', 'attempt_time', 'mailing__owner']
    readonly_fields = ['attempt_time', 'status', 'server_response', 'mailing']

    def server_response_preview(self, obj):
        return obj.server_response[:50] + '...' if obj.server_response and len(
            obj.server_response) > 50 else obj.server_response

    server_response_preview.short_description = 'Ответ сервера'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(mailing__owner=request.user)

    def has_add_permission(self, request):
        # Запрещаем создавать логи вручную
        return False

    def has_change_permission(self, request, obj=None):
        # Запрещаем редактировать логи
        return False


# Регистрируем модели с кастомными админ-классами
admin.site.register(Client, ClientAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Mailing, MailingAdmin)
admin.site.register(MailingLog, MailingLogAdmin)
