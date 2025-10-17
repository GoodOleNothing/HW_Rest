from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """
    Разрешает доступ пользователям из группы 'Moderator'
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name='Moderator').exists()

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsOwner(BasePermission):
    """
    Проверяет, является ли пользователь владельцем объекта
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
