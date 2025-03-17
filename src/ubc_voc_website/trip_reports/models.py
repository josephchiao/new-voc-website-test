from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation

from trips.models import Trip
from comment.models import Comment

class TripReport(models.model):
    class TripReportStatus(models.TextChoices):
        DRAFT = "D",
        PUBLISHED = "P"

    trip = models.OneToOneField(
        Trip,
        on_delete=models.PROTECT
    )
    title = models.CharField(max_length=128, blank=False)
    authors = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="written_trip_reports",
        blank=False
    )
    status = models.CharField(
        max_length=1,
        choices=TripReportStatus,
        default=TripReportStatus.DRAFT
    )
    content = models.TextField(null=False)
    comments = GenericRelation(Comment)

