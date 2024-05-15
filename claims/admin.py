from django.contrib import admin
from .models import *


@admin.register(Orders)
class Orders(admin.ModelAdmin):
    icon_name = 'Claims'
    list_display = ('order_id', 'user', 'product', 'status', 'cr_on')

    def get_queryset(self, request):
        qs = super(Orders, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
