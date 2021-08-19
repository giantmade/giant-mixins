from urllib.parse import parse_qs, urlparse

from django.core.validators import URLValidator
from django.db import models
from django.db.models.functions import Now
from django.utils import timezone

from filer.fields.file import FilerFileField

from .fields import AutoDateTimeField

__all__ = [
    "TimestampMixin",
    "PublishingQuerySetMixin",
    "PublishingMixin",
    "VideoURLMixin",
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

    def published(self, user=None):
        """
        Return the published queryset, or all if user is admin
        """
        if user and user.is_staff:
            return self.all()

        return self.filter(is_published=True, publish_at__lte=Now())


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


class VideoURLMixin(models.Model):
    """
    Mixin to strip the youtube url down and retrieve the video ID
    """

    youtube_url = models.URLField(
        blank=True,
        null=True,
        help_text="""
            Enter the full URL of the youtube video page. 
            To start the video at a specific time add '?start=xx' to the end of the url (using seconds). 
            You can also add extra paramaters using an ampersand, for example '?start=75&autoplay=1'.
        """,
        validators=[
            URLValidator(
                schemes=["https"],
                regex="www.youtube.com",
                message="Please enter the full URL of the Youtube video page",
            )
        ],
    )
    alternate_url = models.URLField(
        blank=True,
        null=True,
        help_text="This will be used if no Youtube URL is provided",
    )

    class Meta:
        abstract = True

    def youtube_video_url(self):
        """
        Get the video ID from the youtube URL
        """
        video_id = parse_qs(urlparse(self.youtube_url).query["v"][0])

        return f"https://www.youtube.com/embed/{video_id}?rel=0&autoplay=1"

    def get_absolute_url(self):
        """
        Returns the url in order of importance
        """
        if self.youtube_url:
            return self.youtube_video_url()
        return self.alternate_url


class URLMixin(models.Model):
    """
    Helper mixin to add internal and external url's to a model
    Requires django-cms to be installed
    """

    # We import here to avoid an error when loading the file. This will only error if cms is not installed and
    # the URLMixin attempts to be loaded
    from cms.models.fields import PageField

    external_url = models.URLField(
        blank=True, help_text="Overrides the internal link if set"
    )
    internal_link = PageField(related_name="+", blank=True, null=True)
    file = FilerFileField(
        related_name="%(app_label)s_%(class)s_files",
        verbose_name="File",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        abstract = True

    def get_absolute_url(self):
        """
        Returns the URL's in order of importance
        """
        if self.external_url:
            return self.external_url
        if self.internal_link:
            return self.internal_link.get_public_url()
        return None

    def file_url(self):
        """
        Returns the file url
        """
        return self.file.url
