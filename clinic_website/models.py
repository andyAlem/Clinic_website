from django.conf import settings
from django.db import models
from django.utils import timezone


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
