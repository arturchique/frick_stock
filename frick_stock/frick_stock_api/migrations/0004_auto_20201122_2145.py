# Generated by Django 3.1.2 on 2020-11-22 18:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('frick_stock_api', '0003_auto_20201122_2144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='follows',
            field=models.ManyToManyField(blank=True, help_text='Подписки', null=True, related_name='followers', to='frick_stock_api.Client', verbose_name='Подписки'),
        ),
        migrations.AlterField(
            model_name='client',
            name='photos',
            field=models.OneToOneField(blank=True, help_text='Фотографии', null=True, on_delete=django.db.models.deletion.CASCADE, to='frick_stock_api.photos', verbose_name='Фотографии'),
        ),
    ]
