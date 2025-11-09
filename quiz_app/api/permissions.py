from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

class IsOwner(permissions.BasePermission):
    """
    "Allows access only for the owner of an object."
    """
    def has_object_permission(self, request, view, obj):

        return obj.owner == request.user