from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import FileResponse
from django.conf import settings
from drf_spectacular.utils import extend_schema, OpenApiExample
from .services import download_video, download_audio
from .models import DownloadedMedia
from .serializers import DownloadMediaSerializer, DownloadedMediaSerializer
import os

class DownloadMediaView(APIView):
    @extend_schema(
        request=DownloadMediaSerializer,
        responses={201: DownloadedMediaSerializer},
        description="YouTube yoki Instagram dan video/audio yuklab olish",
        examples=[
            OpenApiExample(
                'YouTube video',
                value={
                    'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                    'platform': 'youtube',
                    'media_type': 'video'
                }
            ),
            OpenApiExample(
                'Instagram video',
                value={
                    'url': 'https://www.instagram.com/reel/...',
                    'platform': 'instagram',
                    'media_type': 'video'
                }
            ),
            OpenApiExample(
                'YouTube audio',
                value={
                    'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                    'platform': 'youtube',
                    'media_type': 'audio'
                }
            ),
        ]
    )
    def post(self, request):
        serializer = DownloadMediaSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        url = serializer.validated_data['url']
        platform = serializer.validated_data['platform']
        media_type = serializer.validated_data['media_type']

        try:
            # Video yoki audio yuklab olish
            if media_type == 'video':
                file_path = download_video(url, platform)
            else:
                file_path = download_audio(url, platform)

            # Ma'lumotlar bazasiga saqlash
            media = DownloadedMedia.objects.create(
                url=url,
                platform=platform,
                media_type=media_type,
                file_path=file_path,
                title=os.path.basename(file_path)
            )

            response_serializer = DownloadedMediaSerializer(
                media,
                context={'request': request}
            )

            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DownloadFileView(APIView):
    """Yuklangan faylni to'g'ridan-to'g'ri yuklab olish"""

    @extend_schema(
        description="Yuklangan video/audio faylni serverdan yuklab olish",
        responses={200: bytes}
    )
    def get(self, request, media_id):
        try:
            media = DownloadedMedia.objects.get(id=media_id)
            file_path = os.path.join(settings.MEDIA_ROOT, media.file_path)

            if not os.path.exists(file_path):
                return Response(
                    {'error': 'Fayl topilmadi'},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Faylni yuklab olish uchun qaytarish
            response = FileResponse(
                open(file_path, 'rb'),
                content_type='application/octet-stream'
            )
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'

            return response

        except DownloadedMedia.DoesNotExist:
            return Response(
                {'error': 'Media topilmadi'},
                status=status.HTTP_404_NOT_FOUND
            )