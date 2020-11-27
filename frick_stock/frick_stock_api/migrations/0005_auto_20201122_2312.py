# Generated by Django 3.1.2 on 2020-11-22 20:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('frick_stock_api', '0004_auto_20201122_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lot',
            name='buyer',
            field=models.ForeignKey(blank=True, help_text='Покупатели лота', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lots_bought', to='frick_stock_api.client', verbose_name='Покупатели лота'),
        ),
        migrations.AlterField(
            model_name='lot',
            name='likes',
            field=models.ManyToManyField(blank=True, help_text='Лайкнули', null=True, related_name='liked', to='frick_stock_api.Client', verbose_name='Лайкнули'),
        ),
        migrations.AlterField(
            model_name='lot',
            name='media',
            field=models.OneToOneField(blank=True, help_text='Фотографии', null=True, on_delete=django.db.models.deletion.CASCADE, to='frick_stock_api.photos', verbose_name='Фотографии'),
        ),
        migrations.AlterField(
            model_name='lot',
            name='price',
            field=models.OneToOneField(blank=True, help_text='Цена', null=True, on_delete=django.db.models.deletion.CASCADE, to='frick_stock_api.price', verbose_name='Цена'),
        ),
    ]
