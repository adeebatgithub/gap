from django.contrib import admin

from .models import *


@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at")
