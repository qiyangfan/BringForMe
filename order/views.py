from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from media_manager.models import Image
from user.models import Address
from .models import Order


class AddressModelSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = 'OrderAddressModelSerializer'
        model = Address
        fields = ['tag', 'country', 'province', 'city', 'address',
                  'remark', 'postcode', 'contact_person', 'country_code', 'phone']


class OrderModelSerializer(serializers.ModelSerializer):
    destination = AddressModelSerializer()
    image_urls = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'user_id', 'created_at', 'updated_at', 'destination',
                  'description', 'commission', 'status', 'acceptor', 'images',
                  'image_urls']
        extra_kwargs = {
            'id': {'read_only': True},
            'user_id': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'status': {'source': 'get_status_display'},
            'images': {'write_only': True},
            'image_urls': {'read_only': True}
        }

    def get_image_urls(self, obj):
        image_ids = obj.images
        image_urls = []
        if not image_ids:
            return image_urls
        for image_id in image_ids:
            image = Image.objects.get(id=image_id)
            image_urls.append(image.image.url)
        return image_urls


# Create your views here.
class OrderCreateReadView(GenericAPIView):
    serializer_class = OrderModelSerializer

    def get(self, request, *args, **kwargs):
        orders = Order.objects.filter(**request.query_params)
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


class OrderUpdateDeleteView(GenericAPIView):
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
