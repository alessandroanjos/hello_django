from django.contrib import admin
from core.models import Evento

# Register your models here.

class AdminEvento(admin.ModelAdmin):
    list_display = ('titulo', 'data_criacao')
    list_filter = ('titulo',)

admin.site.register(Evento, AdminEvento)
