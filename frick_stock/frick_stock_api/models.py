from django.db import models
import uuid
from django.contrib.auth import get_user_model
from datetime import datetime

USER = get_user_model()

CLIENT_STATUS_CHOICES = (
    ("b", "buyer"),
    ("s", "seller"),
)

PRICE_KIND_CHOICES = (
    ("f", "fast"),
    ("l", "long"),
)


class Photos(models.Model):
    big_photo = models.ImageField(verbose_name="Большая фотография", help_text="Большая фотография")
    little_photo = models.ImageField(verbose_name="Маленькая фотография", help_text="Маленькая фотография")
    header_photo = models.ImageField(verbose_name="Фотография шапки", help_text="Фотография шапки")


class Client(models.Model):
    user = models.OneToOneField(USER, verbose_name="Пользователь", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Имя", help_text="Имя", max_length=40)
    status = models.CharField(verbose_name="Статус", help_text="Статус", max_length=1, choices=CLIENT_STATUS_CHOICES)
    rating = models.FloatField(verbose_name="Рейтинг", help_text="Рейтинг")
    follows = models.ManyToManyField("self", verbose_name="Подписки", help_text="Подписки",
                                     symmetrical=False, related_name="followers")
    bio = models.CharField(verbose_name="Краткая информация", help_text="Краткая информация", max_length=200)
    about = models.TextField(verbose_name="Информация о профиле", help_text="Информация о профиле")
    photos = models.OneToOneField(Photos, verbose_name="Фотографии", help_text="Фотографии", on_delete=models.CASCADE)


class Price(models.Model):
    needed = models.FloatField(verbose_name="Нужно денег", help_text="Нужно денег")
    has = models.FloatField(verbose_name="Имеется денег", help_text="Имеется денег")
    kind = models.CharField(max_length=1, choices=PRICE_KIND_CHOICES, verbose_name="Вид оплаты", help_text="Вид оплаты")
    donators = models.ManyToManyField(Client, verbose_name="Донатеры", help_text="Донатеры", related_name="donated")


class Lot(models.Model):
    name = models.CharField(verbose_name="Название лота", help_text="Название лота", max_length=100)
    description = models.TextField(verbose_name="Описание лота", help_text="Описание лота")
    media = models.OneToOneField(Photos, on_delete=models.CASCADE, verbose_name="Фотографии", help_text="Фотографии")
    price = models.OneToOneField(Price, on_delete=models.CASCADE, verbose_name="Цена", help_text="Цена")
    owner = models.OneToOneField(Client, on_delete=models.CASCADE, verbose_name="Владелец лота",
                                 help_text="Владец лота")
    buyer = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Покупатели лота",
                              help_text="Покупатели лота", related_name="lots_bought")
    likes = models.ManyToManyField(Client, verbose_name="Лайкнули", help_text="Лайкнули", related_name="liked")
