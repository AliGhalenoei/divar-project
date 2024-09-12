from django.contrib import admin

from .models import *
# Register your models here.


@admin.register(SaveAdvertisement)
class SaveAdvertisementAdmin(admin.ModelAdmin):
    list_display = ['user' , 'advertisement']

@admin.register(NoteAdvertisement)
class NoteAdvertisementAdmin(admin.ModelAdmin):
    list_display = ['user' , 'advertisement']

@admin.register(ViewAdvertisement)
class ViewAdvertisementAdmin(admin.ModelAdmin):
    list_display = ['advertisement']