import mimetypes
import os

from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from media_manager.models import Image, Video


# Create your views here.
class ImageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image']
        extra_kwargs = {
            'id': {'read_only': True}
        }


class ImageView(GenericAPIView):
    serializer_class = ImageModelSerializer
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        images = request.FILES.getlist('images')
        data_list = []
        error_list = []
        for image in images:
            serializer = self.get_serializer(data={'image': image})
            if serializer.is_valid():
                serializer.save()
                data_list.append(serializer.data)
            else:
                error_list.append(serializer.errors)
        if error_list:
            return Response({'status': 'error', 'message': error_list}, status=422)
        return Response({'status': 'ok', 'data': data_list})


ALLOWED_VIDEO_EXTENSIONS = {".mp4", ".avi", ".mov", ".mkv"}
ALLOWED_VIDEO_MIME_TYPES = {"video/mp4", "video/avi", "video/quicktime", "video/x-matroska"}


class VideoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'video']
        extra_kwargs = {
            'id': {'read_only': True}
        }

    def validate_video(self, value):
        ext = os.path.splitext(value.name)[1].lower()
        allowed_extensions = {".mp4", ".webm", ".ogv"}
        if ext not in allowed_extensions:
            raise serializers.ValidationError("Unsupported file extension.")

        mime_type, _ = mimetypes.guess_type(value.name)
        allowed_mime_types = ['video/mp4', 'video/webm', 'video/ogg']
        if mime_type not in allowed_mime_types:
            raise serializers.ValidationError("Unsupported video type.")
        return value


class VideoView(GenericAPIView):
    serializer_class = VideoModelSerializer
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        videos = request.FILES.getlist('videos')
        data_list = []
        error_list = []
        for video in videos:
            serializer = self.get_serializer(data={'video': video})
            if serializer.is_valid():
                serializer.save()
                data_list.append(serializer.data)
            else:
                error_list.append(serializer.errors)
        if error_list:
            return Response({'status': 'error', 'message': error_list}, status=422)
        return Response({'status': 'ok', 'data': data_list})
