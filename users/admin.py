from django.contrib import admin
from users.models import *


@admin.register(Admins)
class Admin(admin.ModelAdmin):
    icon_name = 'Admin'
    list_display = ('user', 'phone_number', 'job_title', 'cr_by', 'cr_on')

    def get_queryset(self, request):
        qs = super(Admin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)


@admin.register(Operators)
class Operators(admin.ModelAdmin):
    icon_name = 'Admin'
    list_display = ('user', 'phone_number', 'email', 'cr_on')

    def get_queryset(self, request):
        qs = super(Operators, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)


@admin.register(Clients)
class Client(admin.ModelAdmin):
    icon_name = 'Clients'
    list_display = ('user', 'phone_number', 'email', 'cr_on')

    def get_queryset(self, request):
        qs = super(Client, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
