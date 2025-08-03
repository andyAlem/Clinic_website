import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from clinic_website.models import Appointment
from users.models import CustomUser


class Command(BaseCommand):
    help = "Создаёт тестовых пользователей, модераторов и записи к врачам"

    def handle(self, *args, **kwargs):
        # Создание обычных пользователей
        user1 = CustomUser.objects.create_user(
            email="user1@example.com",
            password="password123",
            first_name="Андрей",
            last_name="Иванов",
        )
        user2 = CustomUser.objects.create_user(
            email="user2@example.com",
            password="password123",
            first_name="Мария",
            last_name="Петрова",
        )

        # Создание модератора
        moderator = CustomUser.objects.create_user(
            email="moderator@example.com",
            password="moderator123",
            first_name="Мод",
            last_name="Ератор",
            is_moderator=True,
        )

        # Создание записей
        for user in [user1, user2]:
            for i in range(2):
                Appointment.objects.create(
                    patient=user,
                    full_name=f"{user.first_name} {user.last_name}",
                    phone=f"+7 (900) 000-00-0{i}",
                    email=user.email,
                    date=timezone.now() + timedelta(days=i + 1),
                    comment="Тестовая запись",
                    status=random.choice(["pending", "confirmed", "cancelled"]),
                )

        self.stdout.write(
            self.style.SUCCESS(
                "✅ Тестовые пользователи, модераторы и записи успешно созданы."
            )
        )
