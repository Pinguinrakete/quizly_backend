from rest_framework import permissions
from rest_framework import authentication, exceptions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


class IsOwner(permissions.BasePermission):
    """
    "Allows access only for the owner of an object."
    """
    def has_object_permission(self, request, view, obj):

        return obj.owner == request.user
    

class CookieJWTAuthentication(authentication.BaseAuthentication):
    """
    "CookieJWTAuthentication authenticates users by reading a JWT access
    token from the access_token cookie, validating it with SimpleJWT
    and returning the associated user for protected API requests."
    """
    cookie_name = "access_token"

    def authenticate(self, request):
        token = request.COOKIES.get(self.cookie_name)

        if not token:
            return None

        jwt_auth = JWTAuthentication()

        try:
            validated_token = jwt_auth.get_validated_token(token)
            user = jwt_auth.get_user(validated_token)
        except (InvalidToken, TokenError):
            raise exceptions.AuthenticationFailed(
                "Invalid or expired token"
                )

        return (user, validated_token)
