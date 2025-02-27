from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.models import Address
from .models import Order


class AddressModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['tag', 'country', 'province', 'city', 'address',
                  'remark', 'postcode', 'contact_person', 'country_code', 'phone']


class OrderModelSerializer(serializers.ModelSerializer):
    destination = AddressModelSerializer()

    class Meta:
        model = Order
        fields = ['id', 'user_id', 'created_at', 'updated_at', 'destination',
                  'description', 'commission', 'status', 'acceptor']
        kwargs = {
            'id': {'read_only': True},
            'user_id': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'status': {'source': 'get_status_display'},
        }


# Create your views here.
class OrderCreateReadView(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = OrderModelSerializer

    def get(self, request, *args, **kwargs):
        orders = Order.objects.all()
        serializer = self.get_serializer(orders, many=True)
        return Response({'status': 'ok', 'data': serializer.data})

    def post(self, request, *args, **kwargs):
        if not request.user:
            raise AuthenticationFailed('Authentication failed.')
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_id=request.user.id)
        else:
            return Response({'status': 'error', 'message': serializer.errors}, status=422)
        return Response({'status': 'ok'})


class OrderUpdateView(GenericAPIView):
    serializer_class = OrderModelSerializer

    def patch(self, request, *args, **kwargs):
        order = Order.objects.get(id=kwargs['id'])
        if order.user_id != request.user.id:
            raise AuthenticationFailed('Authentication failed.')
        serializer = self.get_serializer(instance=order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response({'status': 'error', 'message': serializer.errors}, status=422)
        return Response({'status': 'ok'})

    def delete(self, request, *args, **kwargs):
        order = Order.objects.get(id=kwargs['id'])
        if order.user_id != request.user.id:
            raise AuthenticationFailed('Authentication failed.')
        if order.status == 0:
            return Response({'status': 'error', 'message': 'Order has been accepted.'}, status=403)
        order.delete()
        return Response({'status': 'ok'})
