from django.db import models

class DownloadedMedia(models.Model):
    PLATFORM_CHOICES = [
        ('youtube', 'YouTube'),
        ('instagram', 'Instagram'),
    ]

    TYPE_CHOICES = [
        ('video', 'Video'),
        ('audio', 'Audio'),
    ]

    url = models.URLField(max_length=500)
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    media_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    file_path = models.CharField(max_length=500)
    title = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.platform} - {self.media_type} - {self.title}"

    @property
    def file_url(self):
        from django.conf import settings
        return f"{settings.MEDIA_URL}{self.file_path}"
