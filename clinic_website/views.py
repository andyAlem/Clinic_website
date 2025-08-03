from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import (CreateView, DeleteView, ListView,
                                  TemplateView, UpdateView)
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .forms import AppointmentForm
from .models import Appointment, Service, TeamMember
from .permissions import IsOwnerOrModerator
from .serializers import AppointmentSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    """Представление для работы с записями."""

    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]

    def get_queryset(self):
        user = self.request.user
        if user.is_moderator:
            return Appointment.objects.all().order_by("-date")
        return Appointment.objects.filter(patient=user).order_by("-date")

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)


# --- HTML Views ---
class AppointmentCreateView(CreateView):
    """Представление для создания записи."""

    model = Appointment
    form_class = AppointmentForm
    template_name = "clinic_website/appointment_form.html"
    success_url = reverse_lazy("clinic_website:appointment_success")

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.patient = self.request.user
        return super().form_valid(form)


class AppointmentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Представление для редактирования записи."""

    model = Appointment
    form_class = AppointmentForm
    template_name = "clinic_website/appointment_form.html"
    success_url = reverse_lazy("clinic_website:appointments_list")

    def test_func(self):
        appointment = self.get_object()
        return appointment.patient == self.request.user


class AppointmentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Представление для удаления записи."""

    model = Appointment
    template_name = "clinic_website/appointment_confirm_delete.html"
    success_url = reverse_lazy("clinic_website:appointments_list")

    def test_func(self):
        appointment = self.get_object()
        return appointment.patient == self.request.user


class StaticPageView(TemplateView):
    """Представление для статических страниц."""

    template_name = ""


class AppointmentListView(LoginRequiredMixin, ListView):
    """Представление для списка записей."""

    model = Appointment
    template_name = "clinic_website/appointments_list.html"
    context_object_name = "appointments"

    def get_queryset(self):
        return Appointment.objects.filter(patient=self.request.user).order_by("-date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        appointments = context["appointments"]
        for appointment in appointments:
            appointment.can_edit = (appointment.patient == user) or getattr(
                user, "is_moderator", False
            )
        return context


class ModeratorRequiredMixin:
    """Миксин для проверки, что пользователь является модератором."""

    @method_decorator(user_passes_test(lambda u: u.is_authenticated and u.is_moderator))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ModeratorPanelView(ModeratorRequiredMixin, ListView):
    """Представление для панели модератора."""

    model = Appointment
    template_name = "clinic_website/moderator_panel.html"
    context_object_name = "appointments"

    def get_queryset(self):
        return Appointment.objects.order_by("-date")


class ConfirmAppointmentView(ModeratorRequiredMixin, View):
    """Представление для подтверждения записи."""

    def get(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        appointment.status = "confirmed"
        appointment.save()
        return redirect("clinic_website:moderator_panel")


class CancelAppointmentView(ModeratorRequiredMixin, View):
    """Представление для отмены записи."""

    def get(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        appointment.status = "cancelled"
        appointment.save()
        return redirect("clinic_website:moderator_panel")


class IndexView(TemplateView):
    """Представление для главной страницы."""

    template_name = "clinic_website/index.html"


####
class AboutView(TemplateView):
    """"""

    template_name = "clinic_website/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["team"] = TeamMember.objects.all()
        return context


class ServicesView(ListView):
    model = Service
    template_name = "clinic_website/services.html"
    context_object_name = "services"


class ContactsView(TemplateView):
    template_name = "clinic_website/contacts.html"


class AccountView(LoginRequiredMixin, TemplateView):
    template_name = "clinic_website/account.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["appointments"] = Appointment.objects.filter(
            patient=self.request.user
        ).order_by("-date")
        return context


@login_required
def diagnosis_results_view(request):
    """Результаты диагностики"""
    context = {
        "message": "Результаты обследований пока отсутствуют.",
    }
    return render(request, "clinic_website/diagnosis_results.html", context)
