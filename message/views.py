from django.db.models import Q
from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from user.models import User
from .models import Message


class MessageReceiverSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nickname']


# Create your views here.
class MessageReceiverView(GenericAPIView):
    serializer_class = MessageReceiverSerializer

    def get(self, request, *args, **kwargs):
        sender_id = request.user.id
        receiver_ids = Message.objects.filter(sender_id=sender_id).values_list('receiver_id', flat=True).distinct()
        print(receiver_ids)
        instance = User.objects.filter(id__in=receiver_ids)
        serializer = self.get_serializer(instance, many=True)
        return Response({'status': 'ok', 'data': serializer.data})


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source='sender.nickname', read_only=True)
    receiver = serializers.CharField(source='receiver.nickname', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'created_at']
        extra_kwargs = {
            'id': {'read_only': True},
            'created_at': {'read_only': True},
        }


class MessageView(GenericAPIView):
    serializer_class = MessageSerializer

    def get(self, request, *args, **kwargs):
        sender_id = request.user.id
        receiver_id = kwargs.get('receiver_id')
        instance = (Message.objects.filter(
            Q(sender_id=sender_id, receiver_id=receiver_id) | Q(sender_id=receiver_id, receiver_id=sender_id))
                    .order_by('created_at'))
        serializer = self.get_serializer(instance=instance, many=True)
        return Response({'status': 'ok', 'data': serializer.data})

    def post(self, request, *args, **kwargs):
        receiver_id = kwargs.get('receiver_id')
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(sender_id=request.user.id, receiver_id=receiver_id)
        else:
            return Response({'message': serializer.errors}, status=422)
        return Response({'status': 'ok'})
