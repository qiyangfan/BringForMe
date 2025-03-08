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

    def get(self, request, *args, **kwargs):
        instance = Image.objects.all()
        image_ids = request.query_params.getlist('image_ids')
        print(image_ids)

        if image_ids:
            instance = instance.filter(id__in=image_ids)
        serializer = self.get_serializer(instance, many=True)
        return Response({'status': 'ok', 'data': serializer.data})

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

    def delete(self, request, *args, **kwargs):
        image_ids = request.data.getlist('image_ids')
        print(image_ids)
        if not image_ids:
            return Response({'status': 'error', 'message': 'Image IDs are required.'}, status=422)
        Image.objects.filter(id__in=image_ids).delete()
        return Response({'status': 'ok'})


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


class CreateVideoView(GenericAPIView):
    serializer_class = VideoModelSerializer
    parser_classes = [MultiPartParser]

    def get(self, request, *args, **kwargs):
        instance = Video.objects.all()
        video_ids = request.query_params.get('video_ids')
        if video_ids:
            instance = instance.filter(id__in=video_ids)
        serializer = self.get_serializer(instance, many=True)
        return Response({'status': 'ok', 'data': serializer.data})

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

    def delete(self, request, *args, **kwargs):
        video_ids = request.data.getlist('video_ids')
        if not video_ids:
            return Response({'status': 'error', 'message': 'Image IDs are required.'}, status=422)
        Image.objects.filter(id__in=video_ids).delete()
        return Response({'status': 'ok'})
