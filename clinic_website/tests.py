import pytest
from django.urls import reverse
from django.utils import timezone

from clinic_website.models import Appointment
from users.models import CustomUser


@pytest.mark.django_db
class TestAppointmentViews:
    """
    Тестирование представлений"""

    @pytest.fixture(autouse=True)
    def setup_user(self):
        self.user = CustomUser.objects.create_user(
            email="user@example.com", password="password123"
        )
        self.user2 = CustomUser.objects.create_user(
            email="other@example.com", password="password123"
        )

    def test_appointments_list_requires_login(self, client):
        response = client.get(reverse("clinic_website:appointments_list"))
        assert response.status_code in (301, 302)

    def test_appointments_list_shows_only_own(self, client):
        Appointment.objects.create(
            patient=self.user,
            full_name="One",
            phone="111",
            email="a@a.com",
            date=timezone.now(),
            comment="",
            status="pending",
        )
        Appointment.objects.create(
            patient=self.user2,
            full_name="Two",
            phone="222",
            email="b@b.com",
            date=timezone.now(),
            comment="",
            status="pending",
        )
        client.login(email="user@example.com", password="password123")
        response = client.get(reverse("clinic_website:appointments_list"))
        content = response.content.decode()
        assert "One" in content
        assert "Two" not in content

    def test_make_appointment_get(self, client):
        client.login(email="user@example.com", password="password123")
        response = client.get(reverse("clinic_website:make_appointment"))
        assert response.status_code == 200
        assert "Запись на приём" in response.content.decode()

    def test_make_appointment_post_creates(self, client):
        client.login(email="user@example.com", password="password123")
        data = {
            "full_name": "Иван Иванов",
            "phone": "+70000000000",
            "email": "ivan@example.com",
            "date": timezone.now().strftime("%Y-%m-%dT%H:%M"),
            "comment": "Комментарий",
        }
        response = client.post(reverse("clinic_website:make_appointment"), data)
        assert response.status_code == 302
        assert Appointment.objects.filter(
            patient=self.user, full_name="Иван Иванов"
        ).exists()

    def test_edit_and_delete_permissions(self, client):
        appointment = Appointment.objects.create(
            patient=self.user,
            full_name="One",
            phone="111",
            email="a@a.com",
            date=timezone.now(),
            comment="",
            status="pending",
        )
        url_edit = reverse("clinic_website:appointment_edit", args=[appointment.pk])
        url_delete = reverse("clinic_website:appointment_delete", args=[appointment.pk])

        client.login(email="other@example.com", password="password123")
        res1 = client.get(url_edit)
        assert res1.status_code in (403, 302)
        res2 = client.get(url_delete)
        assert res2.status_code in (403, 302)

        client.login(email="user@example.com", password="password123")
        assert client.get(url_edit).status_code == 200

        response = client.post(url_delete)
        assert response.status_code == 302
        assert not Appointment.objects.filter(pk=appointment.pk).exists()
