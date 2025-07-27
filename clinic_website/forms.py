from django import forms
from django.contrib.auth.forms import AuthenticationForm

from users.models import CustomUser

from .models import Appointment


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email", widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    password = forms.CharField(
        label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-control"})
    )


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    password2 = forms.CharField(
        label="Подтвердите пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name")
        labels = {
            "email": "Электронная почта",
            "first_name": "Имя",
            "last_name": "Фамилия",
        }
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get("password") != cd.get("password2"):
            raise forms.ValidationError("Пароли не совпадают")
        return cd["password2"]


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["full_name", "phone", "email", "date", "comment"]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "date": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-control"}
            ),
            "comment": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
        labels = {
            "full_name": "ФИО",
            "phone": "Телефон",
            "email": "Электронная почта",
            "date": "Дата и время",
            "comment": "Комментарий",
        }
