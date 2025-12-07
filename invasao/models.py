from django.db import models
from users.models import User


class IntrusionSession(models.Model):
    """
    Model representing an intrusion session for capturing media.
    """
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    target_device = models.CharField(max_length=100)
    status = models.CharField(
        max_length=20,
        choices=[
            ('active', 'Active'),
            ('paused', 'Paused'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
        ],
        default='active'
    )
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Intrusion Session"
        verbose_name_plural = "Intrusion Sessions"
    
    def __str__(self):
        if self.created_by:
            return f"{self.title} - {self.target_device} (by {self.created_by})"
        return f"{self.title} - {self.target_device}"


class CapturedMedia(models.Model):
    """
    Model representing captured media (photos, videos, audio) during an intrusion session.
    """
    MEDIA_TYPE_CHOICES = [
        ('photo', 'Photo'),
        ('video', 'Video'),
        ('audio', 'Audio'),
    ]
    
    session = models.ForeignKey(IntrusionSession, on_delete=models.CASCADE, related_name='captured_media')
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    file = models.FileField(upload_to='invasion_media/')
    caption = models.CharField(max_length=200, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    duration = models.DurationField(null=True, blank=True)  # For video/audio
    file_size = models.PositiveIntegerField(help_text="File size in bytes", null=True, blank=True)
    metadata = models.TextField(blank=True, help_text="JSON formatted metadata")
    
    class Meta:
        verbose_name = "Captured Media"
        verbose_name_plural = "Captured Media"
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.get_media_type_display()} - {self.session.title}"


class IntrusionLog(models.Model):
    """
    Model representing logs/events during an intrusion session.
    """
    session = models.ForeignKey(IntrusionSession, on_delete=models.CASCADE, related_name='logs')
    event_type = models.CharField(max_length=50)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    severity = models.CharField(
        max_length=10,
        choices=[
            ('info', 'Info'),
            ('warning', 'Warning'),
            ('error', 'Error'),
            ('critical', 'Critical'),
        ],
        default='info'
    )
    
    class Meta:
        verbose_name = "Intrusion Log"
        verbose_name_plural = "Intrusion Logs"
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.event_type} - {self.session.title}"