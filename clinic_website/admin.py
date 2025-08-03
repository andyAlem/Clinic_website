from django.contrib import admin

from .models import Appointment, DiagnosisNote


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "date", "status", "patient")
    list_filter = ("status", "date")
    search_fields = ("full_name", "email", "phone")


@admin.register(DiagnosisNote)
class DiagnosisNoteAdmin(admin.ModelAdmin):
    list_display = ("patient_name", "created_at", "updated_at")
    search_fields = ("patient_name",)
    ordering = ("-created_at",)
