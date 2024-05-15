from django.contrib import admin
from goods.models import *


@admin.register(Goods)
class Goods(admin.ModelAdmin):
    icon_name = 'Goods'
    list_display = ('id', 'title', 'category', 'amount', 'cr_by', 'cr_on')

    def get_queryset(self, request):
        qs = super(Goods, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)


@admin.register(GoodsCategory)
class GoodsCategory(admin.ModelAdmin):
    icon_name = 'Clients'
    list_display = ('id', 'title', 'cr_by', 'cr_on')

    def get_queryset(self, request):
        qs = super(GoodsCategory, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
