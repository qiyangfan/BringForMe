from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from extensions.permissions import OwnerPermission
from .models import User, Address
from .validators import PasswordValidator


class RegisterModelSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255, validators=[PasswordValidator()])
    confirm_password = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'first_name', 'last_name',
                  'nickname', 'country_code', 'phone', 'email']
        extra_kwargs = {
            'password': {'write_only': True},
            'confirm_password': {'write_only': True},
        }

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
            User.objects.create_user(**serializer.validated_data)
        else:
            return Response({'status': 'error', 'message': serializer.errors}, status=422)
        return Response({'status': 'ok'})


class ChangePasswordModelSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(max_length=255)
    new_password = serializers.CharField(max_length=255, validators=[PasswordValidator()])
    confirm_new_password = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ['old_password', 'new_password', 'confirm_new_password']
        extra_kwargs = {
            'old_password': {'write_only': True},
            'new_password': {'write_only': True},
            'confirm_new_password': {'write_only': True},
        }

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise ValidationError('The old password is incorrect.')
        return value

    def validate_new_password(self, value):
        user = self.context['request'].user
        new_password = self.initial_data.get('new_password')
        if user.check_password(new_password):
            raise ValidationError('The new password cannot be the same as the old password.')
        return value

    def validate_confirm_new_password(self, value):
        new_password = self.initial_data.get('new_password')
        if new_password != value:
            raise ValidationError('The two new passwords are inconsistent.')
        return value


class ChangePasswordView(GenericAPIView):
    permission_classes = [OwnerPermission]
    serializer_class = ChangePasswordModelSerializer

    def patch(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user.set_password(serializer.validated_data.get('new_password'))
            user.save()
        else:
            return Response({'status': 'error', 'message': serializer.errors}, status=422)
        return Response({'status': 'ok'})


class AddressModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'tag', 'country', 'province', 'city',
                  'address', 'remark', 'postcode', 'contact_person', 'country_code',
                  'phone', 'is_default']
        extra_kwargs = {
            'id': {'read_only': True},
        }


class AddressCreateReadView(GenericAPIView):
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


class AddressUpdateDeleteView(GenericAPIView):
    permission_classes = [OwnerPermission]
    serializer_class = AddressModelSerializer

    def patch(self, request, *args, **kwargs):
        user_id = request.user.id
        address_id = kwargs.get('address_id')
        instance = Address.objects.get(id=address_id, user_id=user_id)
        serializer = self.get_serializer(instance=instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response({'status': 'error', 'message': serializer.errors}, status=422)
        return Response({'status': 'ok'})

    def delete(self, request, *args, **kwargs):
        user_id = request.user.id
        address_id = kwargs.get('address_id')
        Address.objects.get(id=address_id, user_id=user_id).delete()
        return Response({'status': 'ok'})


class ProfileModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'nickname',
                  'country_code', 'phone', 'email', ]
        extra_kwargs = {
            'id': {'read_only': True},
            'username': {'read_only': True},
        }


class ProfileView(GenericAPIView):
    permission_classes = [OwnerPermission]
    serializer_class = ProfileModelSerializer

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        serializer = self.get_serializer(User.objects.get(id=user_id))
        return Response({'status': 'ok', 'data': serializer.data})

    def patch(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        instance = User.objects.get(id=user_id)
        serializer = self.get_serializer(instance=instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response({'status': 'error', 'message': serializer.errors}, status=422)
        return Response({'status': 'ok'})
