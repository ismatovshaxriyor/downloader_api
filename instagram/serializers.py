from rest_framework import serializers
from .models import DownloadedMedia

class DownloadMediaSerializer(serializers.Serializer):
    url = serializers.URLField()
    platform = serializers.ChoiceField(choices=['youtube', 'instagram'])
    media_type = serializers.ChoiceField(choices=['video', 'audio'])

class DownloadedMediaSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = DownloadedMedia
        fields = ['id', 'url', 'platform', 'media_type', 'file_path',
                    'file_url', 'title', 'created_at']

    def get_file_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.file_url)
        return obj.file_url
