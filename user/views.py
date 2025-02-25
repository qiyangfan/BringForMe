from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from extensions.permission import OwnerPermission
from .models import User, Address


class RegisterModelSerializer(serializers.ModelSerializer):
    password_validator = RegexValidator(
        r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,20}$',
        r'Your password must be 8-20 characters long and include at least one uppercase letter, one lowercase letter, one number, and one special character (!@#$%^&*).'
    )
    confirm_password = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'first_name', 'last_name', 'nickname', 'phone', 'email']
        extra_kwargs = {
            'password': {'write_only': True},
            'confirm_password': {'write_only': True},
            "first_name": {"required": False},
            "last_name": {"required": False},
        }

    def validate_password(self, value):
        self.password_validator(value)
        return make_password(value)

    def validate_confirm_password(self, value):
        password = self.initial_data.get('password')
        if password != value:
            raise ValidationError('The two passwords are inconsistent.')
        return value


class RegisterView(GenericAPIView):
    authentication_classes = []
    serializer_class = RegisterModelSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data.pop('confirm_password')
            serializer.save()
        else:
            return Response({'status': 'error', 'message': serializer.errors}, status=422)
        return Response({'status': 'ok'})


class AddressModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'tag', 'country', 'province', 'city', 'address', 'remark', 'postcode', 'contact_person',
                  'phone', 'is_default']
        extra_kwargs = {
            'id': {'read_only': True},
        }


class AddressView(GenericAPIView):
    permission_classes = [OwnerPermission]
    serializer_class = AddressModelSerializer

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        queryset = Address.objects.filter(user_id=user_id)
        serializer = self.get_serializer(instance=queryset, many=True)
        user_addresses = serializer.data
        return Response({'status': 'ok', 'data': user_addresses})

    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_id=user_id)
        else:
            return Response({'status': 'error', 'message': serializer.errors}, status=422)
        return Response({'status': 'ok'})


class ProfileModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'nickname', 'phone', 'email', 'balance']
        extra_kwargs = {
            'id': {'read_only': True},
            'username': {'read_only': True},
            'balance': {'read_only': True},
        }


class ProfileView(GenericAPIView):
    permission_classes = [OwnerPermission]
    serializer_class = ProfileModelSerializer

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        serializer = self.get_serializer(User.objects.get(id=user_id))
        return Response({'status': 'ok', 'data': serializer.data})
