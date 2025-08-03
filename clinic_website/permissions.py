from rest_framework import permissions


class IsOwnerOrModerator(permissions.BasePermission):
    """
    - Пациенты могут видеть и редактировать только свои записи.
    - Модераторы могут просматривать, подтверждать и отменять любые записи.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_moderator:
            return True
        return obj.patient == request.user
