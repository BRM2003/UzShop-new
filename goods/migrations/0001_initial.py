# Generated by Django 4.1 on 2023-08-26 09:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GoodsCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=128)),
                ('cr_on', models.DateTimeField(auto_now_add=True)),
                ('up_on', models.DateTimeField(auto_now=True, null=True)),
                ('cr_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='category_cr_by', to=settings.AUTH_USER_MODEL)),
                ('up_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='category_up_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Category',
            },
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('amount', models.IntegerField(default=0)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='goods')),
                ('cr_on', models.DateTimeField(auto_now_add=True)),
                ('up_on', models.DateTimeField(auto_now=True, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='goods.goodscategory')),
                ('cr_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='product_cr_by', to=settings.AUTH_USER_MODEL)),
                ('up_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='product_up_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Good',
                'verbose_name_plural': 'Goods',
            },
        ),
    ]