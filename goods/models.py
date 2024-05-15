from django.db import models
from django.contrib.auth.models import User


class GoodsCategory(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=128)
    cr_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='category_cr_by')
    up_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='category_up_by')
    cr_on = models.DateTimeField(auto_now_add=True)
    up_on = models.DateTimeField(null=True, blank=True, auto_now=True)

    class Meta:
        verbose_name_plural = 'Category'
        verbose_name = 'Category'

    def __str__(self):
        return self.title


class Goods(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=128)
    category = models.ForeignKey(GoodsCategory, on_delete=models.DO_NOTHING)
    description = models.TextField()
    amount = models.IntegerField(default=0)
    price_for_admin = models.IntegerField(default=0)
    currency = models.CharField(max_length=12, default='UZS')
    photo = models.ImageField(upload_to='goods', null=True, blank=True)
    cr_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='product_cr_by')
    up_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='product_up_by')
    cr_on = models.DateTimeField(auto_now_add=True)
    up_on = models.DateTimeField(null=True, blank=True, auto_now=True)

    class Meta:
        verbose_name_plural = 'Goods'
        verbose_name = 'Good'

    def __str__(self):
        return self.title

