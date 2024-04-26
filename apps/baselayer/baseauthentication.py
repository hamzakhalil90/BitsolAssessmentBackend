import jwt
from django.middleware.csrf import CsrfViewMiddleware
from django.views.decorators.csrf import csrf_exempt
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from django.conf import settings


class CSRFCheck(CsrfViewMiddleware):
    def _reject(self, request, reason):
        # Return the failure reason instead of an HttpResponse
        return reason


class UserAuthentication(BaseAuthentication):
    """
    custom authentication class for DRF, Fernet and JWT
    """

    @csrf_exempt
    def authenticate(self, request):
        print(f"Request Path: {request.path}")

        authorization_header = request.headers.get("Authorization")
        if not authorization_header:
            raise exceptions.AuthenticationFailed("User token is required")

        try:
            """DECODE TOKEN"""
            access_token = authorization_header.split(" ")[1]
            payload = jwt.decode(
                access_token, settings.SECRET_KEY, algorithms=["HS256"]
            )
        except IndexError:
            raise exceptions.AuthenticationFailed("Token prefix missing")
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token expired")
        except jwt.InvalidTokenError:
            raise exceptions.NotAcceptable("Invalid token")

        user = None

        if user is None:
            raise exceptions.AuthenticationFailed("User not found")

        return user, None
