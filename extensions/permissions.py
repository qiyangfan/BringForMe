from rest_framework.permissions import BasePermission

from user.models import User


class OwnerPermission(BasePermission):
    def has_permission(self, request, view):
        username = request.user
        user_id = view.kwargs.get('user_id')
        user = User.objects.filter(username=username, id=user_id).first()
        if user is None:
            return False
        return True
