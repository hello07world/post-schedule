from django.db import models

class Post(models.Model):
    STATUS_CHOICES = (
        ('created', 'Created'),
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('published', 'Published'),
        ('deleted', 'Deleted'),
    )
    POST_TYPE_CHOICES = (
        ('simple', 'Simple'),
        ('image', 'Image'),
        ('video', 'Video'),
    )
    # For simplicity, we use a CharField to simulate the user identity.
    user = models.CharField(max_length=100, default="anonymous")
    post_type = models.CharField(max_length=10, choices=POST_TYPE_CHOICES)
    caption = models.TextField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='created')
    scheduled_time = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.post_type} - {self.status}"
