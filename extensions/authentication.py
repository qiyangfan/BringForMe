import jwt
from django.conf import settings
from jwt import exceptions
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            payload = jwt.decode(token, key=settings.SECRET_KEY, algorithms=['HS256'])
        except exceptions.ExpiredSignatureError:
            raise AuthenticationFailed('The token has expired.')
        except jwt.DecodeError:
            raise AuthenticationFailed('The token is invalid.')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('The token is invalid.')
        # request.user = payload, request.auth = token
        return payload, token
