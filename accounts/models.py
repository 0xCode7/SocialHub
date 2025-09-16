from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    PRIVACY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.jpeg')

    # Settings
    privacy = models.CharField(
        max_length=10,
        choices=PRIVACY_CHOICES,
        default='public',
        help_text="Who can see your posts and profile."
    )

    is_visible = models.BooleanField(
        default=True,
        help_text="Show your profile to others."
    )


    # Notify
    notify_on_like = models.BooleanField(
        default=True,
        help_text="Receive notifications when someone likes your post."
    )
    notify_on_comment = models.BooleanField(
        default=True,
        help_text="Receive notifications when someone comments on your post."
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"
