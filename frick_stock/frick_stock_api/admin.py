from django.contrib import admin
from .models import *


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(Lot)
class LotAdmin(admin.ModelAdmin):
    list_display = ('name', )
