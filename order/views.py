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
            'images': {'write_only': True},
            'image_urls': {'read_only': True}
        }

    # Get the image URLs from database according to the image IDs
    def get_image_urls(self, obj):
        image_ids = obj.images
        image_urls = []
        if not image_ids:
            return image_urls
        for image_id in image_ids:
            image = Image.objects.filter(id=image_id).first()
            if image:
                image_urls.append(image.image.url)
        return image_urls

    def validate(self, attrs):
        if attrs.get('status') == 1 and not attrs.get('acceptor'):
            raise serializers.ValidationError('Acceptor is required to accept the order.')
        return attrs


# Create your views here.
class OrderCreateReadView(GenericAPIView):
    serializer_class = OrderModelSerializer

    # Get the order list
    def get(self, request, *args, **kwargs):
        orders = Order.objects.all()
        order_id = request.query_params.get('order_id')
        if request.data.get('order_id'):
            orders = orders.filter(id=order_id)
        serializer = self.get_serializer(orders, many=True)
        return Response({'status': 'ok', 'data': serializer.data})

    # Add a new order
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_id=request.user.id)
        else:
            return Response({'status': 'error', 'message': serializer.errors}, status=422)
        return Response({'status': 'ok'})


class OrderUpdateDeleteView(GenericAPIView):
    serializer_class = OrderModelSerializer

    # Update the order
    def patch(self, request, *args, **kwargs):
        order_id = kwargs['order_id']
        order = Order.objects.filter(id=order_id).first()
        # Check if the order exists
        if not order:
            return Response({'status': 'error', 'message': 'Order does not exist.'}, status=404)
        # Check if the user is the creator or the acceptor of the order
        if order.acceptor_id and request.user.id not in [order.acceptor_id, order.user_id]:
            raise AuthenticationFailed('Authentication failed.')
        serializer = self.get_serializer(instance=order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response({'status': 'error', 'message': serializer.errors}, status=422)
        return Response({'status': 'ok'})

    # Delete the order
    def delete(self, request, *args, **kwargs):
        order_id = kwargs['order_id']
        order = Order.objects.filter(id=order_id).first()
        # Check if the order exists
        if not order:
            return Response({'status': 'error', 'message': 'Order does not exist.'}, status=404)
        # Check if the user is the creator of the order
        if order.user_id != request.user.id:
            raise AuthenticationFailed('Authentication failed.')
        # Check if the order has been accepted
        if order.status == 1:
            return Response({'status': 'error', 'message': 'Order has been accepted.'}, status=403)
        order.delete()
        return Response({'status': 'ok'})
