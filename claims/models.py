from django.db import models
from goods.models import *
from users.models import *


class Orders(models.Model):
    CHOICES_STATUS = (
        ('1', 'Yangi'),
        ('2', 'Qabul qilind'),
        ('3', 'Yetkazilmoqda'),
        ('4', 'Yetqazib berildi'),
        ('5', 'Qaytib kelgan'),
        ('6', "Keyin Oladi"),
        ('7', 'Qayta Qongiroq'),
        ('8', 'Arxiv'),
        ('9', 'Dubl'),
        ('10', 'Ban')
    )
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Clients, on_delete=models.DO_NOTHING, related_name='clients', null=True, blank=True)
    user_name = models.CharField(max_length=128, null=True, blank=True)
    user_phone_number = models.CharField(max_length=128, null=True, blank=True)
    product = models.ForeignKey(Goods, on_delete=models.DO_NOTHING, related_name='products')
    admin = models.ForeignKey(Admins, on_delete=models.DO_NOTHING, related_name='admins', null=True, blank=True)
    operator = models.IntegerField(default=0)
    count_of_products = models.IntegerField(default=1)
    total_amount = models.IntegerField(default=0)
    region = models.CharField(max_length=32, default='uz')
    description = models.CharField(max_length=256, null=True, blank=True)
    comment = models.CharField(max_length=128, null=True, blank=True)
    status = models.CharField(max_length=100, choices=CHOICES_STATUS, default=1)
    cr_on = models.DateTimeField(auto_now_add=True)
    up_on = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Orders'
        verbose_name = 'Order'

    def __int__(self):
        return self.id

