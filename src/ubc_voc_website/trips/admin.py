from django.contrib import admin
from .models import Trip, TripTag

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_time', 'end_time')
    search_fields = ('name',)
    list_filter = ('start_time', 'end_time')

@admin.register(TripTag)
class TripTagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
