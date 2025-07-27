import pytest
from django.urls import reverse

from users.models import CustomUser


@pytest.mark.django_db
class TestAuthViews:
    def test_registration(self, client):
        url = reverse("clinic_website:register")
        data = {
            "email": "new@example.com",
            "password": "pass1234",
            "password2": "pass1234",
        }
        response = client.post(url, data)
        assert response.status_code == 302
        assert CustomUser.objects.filter(email="new@example.com").exists()

    def test_login_logout_flow(self, client):
        user = CustomUser.objects.create_user(
            email="log@example.com", password="password123"
        )
        login_url = reverse("clinic_website:login")
        response = client.post(
            login_url, {"username": user.email, "password": "password123"}
        )
        assert response.status_code == 302
        # после логина доступна страница
        res2 = client.get(reverse("clinic_website:index"))
        assert res2.status_code == 200

        logout_url = reverse("clinic_website:logout")
        res_logout = client.post(logout_url)
        assert res_logout.status_code == 302
