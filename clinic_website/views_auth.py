from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.models import CustomUser

from .forms import UserLoginForm, UserRegistrationForm


class CustomLoginView(LoginView):
    """Вход в систему"""

    template_name = "clinic_website/login.html"
    authentication_form = UserLoginForm
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    """Выход из системы"""

    next_page = reverse_lazy("clinic_website:index")


class RegisterView(CreateView):
    """Регистрация пользователя"""

    model = CustomUser
    form_class = UserRegistrationForm
    template_name = "clinic_website/register.html"
    success_url = reverse_lazy("clinic_website:index")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response
