from django.conf import settings
from django.db import models
from django.utils import timezone

from users.models import CustomUser


class Appointment(models.Model):
    """Запись на приём к врачу"""

    STATUS_CHOICES = [
        ("pending", "В ожидании"),
        ("confirmed", "Подтверждена"),
        ("cancelled", "Отменена"),
    ]

    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="appointments"
    )
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    date = models.DateTimeField()
    comment = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name="Статус записи",
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return (
            f"{self.full_name} - {self.date.strftime('%Y-%m-%d %H:%M')} ({self.status})"
        )


class TeamMember(models.Model):
    """Сотрудник команды"""

    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to="team/", blank=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    """Услуга"""

    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.title


class DiagnosisNote(models.Model):
    """Результаты диагностики"""

    patient_name = models.CharField(max_length=200)
    note_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Заметка для {self.patient_name} ({self.created_at.date()})"
