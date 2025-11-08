from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

class IsOwner(permissions.BasePermission):
    """
    "Allows access only for the owner of an object."
    """
    def has_object_permission(self, request, view, obj):

        return obj.owner == request.user
    

class HeaderOrCookieJWTAuthentication(JWTAuthentication):
    """
    First authenticates via the Authorization header,
    falls back to the cookie ('access_token') if no header is present.
    """
    def authenticate(self, request):
        header = self.get_header(request)
        if header is not None:
            raw_token = self.get_raw_token(header)
            if raw_token is not None:
                validated_token = self.get_validated_token(raw_token)
                return self.get_user(validated_token), validated_token

        raw_token = request.COOKIES.get('access_token')
        if raw_token is not None:
            validated_token = self.get_validated_token(raw_token)
            return self.get_user(validated_token), validated_token

        return None
