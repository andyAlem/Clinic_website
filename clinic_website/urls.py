from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (AppointmentCreateView, AppointmentDeleteView,
                    AppointmentListView, AppointmentUpdateView,
                    AppointmentViewSet, CancelAppointmentView,
                    ConfirmAppointmentView, IndexView, ModeratorPanelView,
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
        "success/",
        StaticPageView.as_view(template_name="clinic_website/success.html"),
        name="appointment_success",
    ),
    path(
        "about/",
        StaticPageView.as_view(template_name="clinic_website/about.html"),
        name="about",
    ),
    path(
        "contacts/",
        StaticPageView.as_view(template_name="clinic_website/contacts.html"),
        name="contacts",
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
