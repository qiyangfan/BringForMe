from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class FailedAuthentication(BaseAuthentication):
    def authenticate(self, request):
        raise AuthenticationFailed('Authentication failed.')

    def authenticate_header(self, request):
        return 'Authentication failed.'
