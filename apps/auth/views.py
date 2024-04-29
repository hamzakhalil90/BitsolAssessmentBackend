import logging
from apps.baselayer.baseapiviews import BaseAPIView
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from rest_framework import status
from apps.users.models import Token, User
from apps.baselayer.response_messages import *
from django.contrib.auth import get_user_model

logger = logging.getLogger(settings.LOGGER_NAME_PREFIX + __name__)


class AuthenticationBackend(object):
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(email__iexact=username)
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None


class LoginView(BaseAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            email = request.data.get("email")
            password = request.data.get("password")
            user = authenticate(username=email, password=password)
            if not user:
                return self.send_bad_request_response(errors_details=INVALID_USERNAME_OR_PASSWORD,
                                                      status_code=status.HTTP_401_UNAUTHORIZED)
            else:
                token = user.get_access_token()
                token, created = Token.objects.get_or_create(user=user, token=token)
                return self.send_success_response(
                    message="Logged in successfully.",
                    data={"token": token.token}
                )
        except Exception as err:
            logger.error(err)
            return self.send_internal_server_error_response(message="Something went wrong!")
