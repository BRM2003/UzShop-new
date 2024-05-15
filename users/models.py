from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Admins(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='admins')
    phone_number = models.CharField(max_length=32)
    job_title = models.CharField(max_length=128)
    photo = models.ImageField(upload_to='users', null=True, blank=True)
    cr_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='admin_cr_by')
    up_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='admin_up_by')
    cr_on = models.DateTimeField(auto_now_add=True)
    up_on = models.DateTimeField(null=True, blank=True, auto_now=True)

    class Meta:
        verbose_name_plural = 'Admins'
        verbose_name = 'Admin'

    def __str__(self):
        return '{} - {}'.format(self.id, self.user)


class Operators(models.Model):
    id = models.AutoField(primary_key=True),
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='operators')
    phone_number = models.CharField(max_length=32)
    email = models.CharField(max_length=128, null=True, blank=True)
    cr_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Operators'
        verbose_name = 'Operator'

    def __int__(self):
        return self.id


class Clients(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='clients')
    phone_number = models.CharField(max_length=32)
    email = models.CharField(max_length=128, null=True, blank=True)
    cr_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Clients'
        verbose_name = 'Client'

    def __str__(self):
        return self.user.username


