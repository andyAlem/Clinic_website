from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views
from .views import (AboutView, AccountView, AppointmentCreateView,
                    AppointmentDeleteView, AppointmentListView,
                    AppointmentUpdateView, AppointmentViewSet,
                    CancelAppointmentView, ConfirmAppointmentView,
                    ContactsView, IndexView, ModeratorPanelView, ServicesView,
                    StaticPageView)
from .views_auth import CustomLoginView, CustomLogoutView, RegisterView

app_name = "clinic_website"

router = DefaultRouter()
router.register(r"appointments", AppointmentViewSet, basename="appointment")

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("api/", include(router.urls)),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("make-appointment/", AppointmentCreateView.as_view(), name="make_appointment"),
    path(
        "appointments/<int:pk>/edit/",
        AppointmentUpdateView.as_view(),
        name="appointment_edit",
    ),
    path(
        "appointments/<int:pk>/delete/",
        AppointmentDeleteView.as_view(),
        name="appointment_delete",
    ),
    path("appointments/", AppointmentListView.as_view(), name="appointments_list"),
    path(
        "diagnosis-results/",
        views.diagnosis_results_view,
        name="view_diagnosis_results",
    ),
    path("account/", AccountView.as_view(), name="account"),  # Личный кабинет
    path("about/", AboutView.as_view(), name="about"),  # О нас
    path("services/", ServicesView.as_view(), name="services"),  # Услуги
    path("contacts/", ContactsView.as_view(), name="contacts"),  # Контакты
    path(
        "success/",
        StaticPageView.as_view(template_name="clinic_website/success.html"),
        name="appointment_success",
    ),
    path("moderator/", ModeratorPanelView.as_view(), name="moderator_panel"),
    path(
        "moderator/confirm/<int:pk>/",
        ConfirmAppointmentView.as_view(),
        name="moderator_confirm",
    ),
    path(
        "moderator/cancel/<int:pk>/",
        CancelAppointmentView.as_view(),
        name="moderator_cancel",
    ),
]
