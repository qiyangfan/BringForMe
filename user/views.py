import re
from datetime import datetime, timezone, timedelta

import jwt
from django import forms
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, Address


class LoginModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']


class LoginView(APIView):
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        target_user = User.objects.filter(email=email).first()
        if target_user is None or not check_password(password, target_user.password):
            return Response({'status': 'error', 'message': 'The email address or password is incorrect.'}, status=400)
        headers = {
            'typ': 'JWT',
            'alg': 'HS256'
        }
        payload = {
            'id': target_user.id,
            'email': target_user.email,
            'exp': datetime.now(timezone.utc) + timedelta(days=1)
        }
        token = jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm='HS256', headers=headers)
        return Response({'status': 'ok', 'token': token})


class RegisterModelForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=255)

    class Meta:
        model = User
        fields = ['email', 'password', 'confirm_password', 'nickname']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        password_re = re.compile(
            r'^(?![a-zA-Z]+$)(?![A-Z0-9]+$)(?![A-Z!@#$%^&*]+$)(?![a-z0-9]+$)(?![a-z!@#$%^&*]+$)(?![0-9!@#$%^&*]+$)[a-zA-Z0-9!@#$%^&*]{8,20}$')
        if not password_re.search(password):
            raise ValidationError(
                'Your password must be 8 to 20 characters long and include at least three of the following: uppercase letters, lowercase letters, numbers, and special symbols (!@#$%^&*).')
        return make_password(password)

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if not check_password(confirm_password, password):
            raise ValidationError('The two passwords are inconsistent.')
        return confirm_password


class RegisterView(APIView):
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        form = RegisterModelForm(request.data)
        if form.is_valid():
            form.save()
        else:
            return Response({'status': 'error', 'message': form.errors}, status=422)
        return Response({'status': 'ok'})


# TODO
class ProfileView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        user_id = user['id']
        return Response({'status': 'ok'})


class AddressModelForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['user', 'tag', 'country', 'province', 'city', 'address', 'remark', 'postcode', 'phone', 'is_default']

    def clean_user_id(self):
        user_id = self.cleaned_data.get('user_id')
        user = User.objects.filter(id=user_id).first()
        if user is None:
            raise ValidationError('The user does not exist.')
        return user_id


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class AddressView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        user_id = user['id']
        queryset = Address.objects.filter(user_id=user_id).all()
        user_addresses = AddressSerializer(queryset, many=True)
        return Response({'status': 'ok', 'data': user_addresses})

    def post(self, request, *args, **kwargs):
        print(request.user)

        form = AddressModelForm({**request.data, 'user': 1})
        if form.is_valid():
            form.save()
        else:
            return Response({'status': 'error', 'message': form.errors}, status=422)
        return Response({'status': 'ok'})
