from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response

from .models import User, Address
from .validators import PasswordValidator


# User model serializer for registration
class RegisterModelSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255, validators=[PasswordValidator()])
    confirm_password = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'first_name', 'last_name',
                  'nickname', 'country_code', 'phone', 'email']
        extra_kwargs = {
            'username': {'write_only': True},
            'password': {'write_only': True},
            'confirm_password': {'write_only': True},
            'first_name': {'write_only': True},
            'last_name': {'write_only': True},
            'nickname': {'write_only': True},
            'country_code': {'write_only': True},
            'phone': {'write_only': True},
            'email': {'write_only': True},
        }

    # Check if the two passwords are inconsistent
    def validate_confirm_password(self, value):
        password = self.initial_data.get('password')
        if password != value:
            raise ValidationError('The two passwords are inconsistent.')
        return value

    # Check if the country code and phone number are filled in together
    def validate(self, attrs):
        country_code = attrs.get('country_code')
        phone = attrs.get('phone')
        if (phone and not country_code) or (country_code and not phone):
            raise ValidationError('The country code and phone number must be filled in together.')
        return attrs


class RegisterView(GenericAPIView):
    authentication_classes = []
    serializer_class = RegisterModelSerializer

    # Register a new user
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Remove the confirm_password field
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

    # Check if the old password is correct
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise ValidationError('The old password is incorrect.')
        return value

    # Check if the new password is the same as the old password
    def validate_new_password(self, value):
        user = self.context['request'].user
        new_password = self.initial_data.get('new_password')
        if user.check_password(new_password):
            raise ValidationError('The new password cannot be the same as the old password.')
        return value

    # Check if the two new passwords are inconsistent
    def validate_confirm_new_password(self, value):
        new_password = self.initial_data.get('new_password')
        if new_password != value:
            raise ValidationError('The two new passwords are inconsistent.')
        return value


class ChangePasswordView(GenericAPIView):
    serializer_class = ChangePasswordModelSerializer

    # Change the password
    def patch(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # Remove the confirm_new_password field
            user.set_password(serializer.validated_data.get('new_password'))
            user.save()
        else:
            return Response({'status': 'error', 'message': serializer.errors}, status=422)
        return Response({'status': 'ok'})


class AddressModelSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = 'UserAddressModelSerializer'
        model = Address
        fields = ['id', 'tag', 'country', 'province', 'city',
                  'address', 'remark', 'postcode', 'contact_person', 'country_code',
                  'phone', 'is_default']
        extra_kwargs = {
            'id': {'read_only': True},
        }


class AddressCreateReadView(GenericAPIView):
    serializer_class = AddressModelSerializer

    # Get the address list of the current user
    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        queryset = Address.objects.filter(user_id=user_id)
        address_id = request.query_params.get('address_id')
        if address_id:
            queryset = queryset.filter(id=address_id)
        serializer = self.get_serializer(instance=queryset, many=True)
        user_addresses = serializer.data
        return Response({'status': 'ok', 'data': user_addresses})

    # Add a new address
    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_id=user_id)
        else:
            return Response({'status': 'error', 'message': serializer.errors}, status=422)
        return Response({'status': 'ok'})


class AddressUpdateDeleteView(GenericAPIView):
    serializer_class = AddressModelSerializer

    # Update the address
    def patch(self, request, *args, **kwargs):
        user_id = request.user.id
        address_id = kwargs.get('address_id')
        print(address_id)
        instance = Address.objects.filter(id=address_id, user_id=user_id).first()
        if not instance:
            return Response({'status': 'error', 'message': 'Address does not exist.'}, status=404)
        serializer = self.get_serializer(instance=instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response({'status': 'error', 'message': serializer.errors}, status=422)
        return Response({'status': 'ok'})

    # Delete the address
    def delete(self, request, *args, **kwargs):
        user_id = request.user.id
        address_id = kwargs.get('address_id')
        try:
            Address.objects.filter(id=address_id, user_id=user_id).delete()
        except Address.DoesNotExist:
            return Response({'status': 'error', 'message': 'Address does not exist.'}, status=404)
        return Response({'status': 'ok'})


class ProfileModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'nickname',
                  'country_code', 'phone', 'email', 'avatar']
        extra_kwargs = {
            'id': {'read_only': True},
            'username': {'read_only': True},
        }


class ProfileView(GenericAPIView):
    serializer_class = ProfileModelSerializer
    parser_classes = [JSONParser, MultiPartParser]

    # Get the profile of the current user
    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        serializer = self.get_serializer(User.objects.get(id=user_id))
        return Response({'status': 'ok', 'data': serializer.data})

    # Update the profile of the current user
    def patch(self, request, *args, **kwargs):
        user_id = request.user.id
        instance = User.objects.get(id=user_id)
        serializer = self.get_serializer(instance=instance, data=request.data, partial=True)
        if serializer.is_valid():
            print(serializer.validated_data)
            serializer.save()
        else:
            return Response({'status': 'error', 'message': serializer.errors}, status=422)
        return Response({'status': 'ok'})


class SimpleProfileModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nickname', 'country_code', 'phone', 'email', 'avatar']
        extra_kwargs = {
            'id': {'read_only': True},
            'nickname': {'read_only': True},
            'country_code': {'read_only': True},
            'phone': {'read_only': True},
            'email': {'read_only': True},
            'avatar': {'read_only': True},
        }


class OtherUserProfileView(GenericAPIView):
    serializer_class = SimpleProfileModelSerializer
    parser_classes = [JSONParser, MultiPartParser]

    # Get the simplified profile of other users
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        instance = User.objects.filter(id=user_id).first()
        if not instance:
            return Response({'status': 'error', 'message': 'User does not exist.'}, status=404)
        serializer = self.get_serializer(instance=instance)
        return Response({'status': 'ok', 'data': serializer.data})


class BatchUserProfileView(GenericAPIView):
    serializer_class = SimpleProfileModelSerializer
    parser_classes = [JSONParser, MultiPartParser]

    # Get the simplified profile of multiple users
    def get(self, request, *args, **kwargs):
        user_ids = request.query_params.getlist('user_ids')
        if not user_ids:
            return Response({'status': 'error', 'message': 'User IDs are required.'}, status=422)
        instance = User.objects.filter(id__in=user_ids)
        if not instance:
            return Response({'status': 'error', 'message': 'Users do not exist.'}, status=404)
        serializer = self.get_serializer(instance=instance, many=True)
        user_profiles = serializer.data
        return Response({'status': 'ok', 'data': user_profiles})
