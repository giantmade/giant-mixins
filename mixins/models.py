from urllib.parse import parse_qs, urlparse

from django.core.validators import URLValidator
from django.db import models
from django.utils import timezone

from .fields import AutoDateTimeField

__all__ = [
    "TimestampMixin",
    "PublishingQuerySetMixin",
    "PublishingMixin",
    "YoutubeURLMixin",
]


class TimestampMixin(models.Model):
    """
    Helper mixin to add a created at and updated field to a model
    """

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = AutoDateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class PublishingQuerySetMixin(models.QuerySet):
    """
    Helper mixin to filter news articles which are published and
    whose date is less than the current date
    """

    def published(self):
        """
        Return the published queryset
        """

        return self.filter(is_published=True, publish_at__lte=timezone.now())


class PublishingMixin(models.Model):
    """
    Helper mixin to add the following fields: is_published, publish_date,
    title, slug
    """

    is_published = models.BooleanField(
        default=False, help_text="Selecting this option will publish this item"
    )
    publish_at = models.DateTimeField(null=True, blank=True, default=timezone.now)

    class Meta:
        abstract = True


class YoutubeURLMixin(models.Model):
    """
    Mixin to strip the youtube url down and retrieve the video ID
    """

    youtube_url = models.URLField(
        help_text="Enter the full URL of the youtube video page",
        validators=[
            URLValidator(
                schemes=["https"],
                regex="www.youtube.com",
                message="Please enter the full URL of the Youtube video page",
            )
        ],
    )

    class Meta:
        abstract = True

    def youtube_video_url(self, youtube_url):
        """
        Get the video ID from the youtube URL
        """
        video_id = parse_qs(urlparse(youtube_url).query["v"][0])

        return f"https://www.youtube.com/embed/{video_id}?rel=0&autoplay=1"
