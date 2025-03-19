from django.db.models import Q
from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response

from user.models import User
from .models import Message


class MessageReceiverSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nickname']
        extra_kwargs = {
            'id': {'read_only': True},
            'nickname': {'read_only': True},
        }


# Create your views here.
class MessageReceiverView(GenericAPIView):
    serializer_class = MessageReceiverSerializer

    # Get the user list who has chatted with the current user
    def get(self, request, *args, **kwargs):
        my_id = request.user.id
        # Get the user IDs who have sent messages to the current user
        receiver_ids = Message.objects.filter(sender_id=my_id).values_list('receiver_id', flat=True).distinct()
        # Get the user IDs who have received messages from the current user
        sender_ids = Message.objects.filter(receiver_id=my_id).values_list('sender_id', flat=True).distinct()
        all_ids = receiver_ids.union(sender_ids)
        # Get the user instances according to the user IDs
        instance = User.objects.filter(id__in=all_ids)
        serializer = self.get_serializer(instance, many=True)
        return Response({'status': 'ok', 'data': serializer.data})


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'created_at', 'image']
        extra_kwargs = {
            'id': {'read_only': True},
            'created_at': {'read_only': True},
            'sender': {'read_only': True},
            'receiver': {'read_only': True},
        }

    def validate(self, attrs):
        if 'content' not in attrs and 'image' not in attrs:
            raise serializers.ValidationError('Content or image is required.')
        return attrs


class MessageView(GenericAPIView):
    serializer_class = MessageSerializer
    parser_classes = [JSONParser, MultiPartParser]

    # Get the message list between the current user and the specified user
    def get(self, request, *args, **kwargs):
        sender_id = request.user.id
        receiver_id = kwargs.get('receiver_id')
        instance = (Message.objects.filter(
            Q(sender_id=sender_id, receiver_id=receiver_id) | Q(sender_id=receiver_id, receiver_id=sender_id))
                    .order_by('created_at'))
        serializer = self.get_serializer(instance=instance, many=True)
        return Response({'status': 'ok', 'data': serializer.data})

    # Send a message to the specified user
    def post(self, request, *args, **kwargs):
        receiver_id = kwargs.get('receiver_id')
        data_list = []
        error_list = []
        # handle the content
        content = request.data.get('content')
        if content:
            serializer = self.get_serializer(data={'content': content})
            if serializer.is_valid():
                serializer.save(sender_id=request.user.id, receiver_id=receiver_id)
                data_list.append(serializer.data)
            else:
                error_list.append(serializer.errors)
        # handle the images
        images = request.FILES.getlist('images')
        if images:
            for image in images:
                serializer = self.get_serializer(data={'image': image})
                if serializer.is_valid():
                    serializer.save(sender_id=request.user.id, receiver_id=receiver_id)
                    data_list.append(serializer.data)
                else:
                    error_list.append(serializer.errors)

        if error_list:
            return Response({'status': 'error', 'message': error_list}, status=422)
        return Response({'status': 'ok', 'data': data_list})
