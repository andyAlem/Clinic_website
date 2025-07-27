from django.contrib import admin

from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "date", "status", "patient")
    list_filter = ("status", "date")
    search_fields = ("full_name", "email", "phone")
