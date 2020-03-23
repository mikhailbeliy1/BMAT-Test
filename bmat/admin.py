from django.contrib import admin

from .models import MusicalWork
# Register your models here.

@admin.register(MusicalWork)

class CustomMusicalWorkAdmin(admin.ModelAdmin):
    list_display = ('title', 'contributors', 'iswc')
