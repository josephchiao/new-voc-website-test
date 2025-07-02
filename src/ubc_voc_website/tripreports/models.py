from django.conf import settings
from django.db import models

from puput.models import Category, Entry
from trips.models import Trip
from wagtail.admin.panels import FieldPanel

class TripReport(Entry):
    trip = models.ForeignKey(Trip, on_delete=models.SET_NULL, null=True, blank=True, related_name="trip_reports")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="trip_reports")
    categories = models.ManyToManyField(
        Category,
        through='TripReportCategoryEntryPage',
        blank=True
    )
    content_panels = Entry.content_panels + [
        FieldPanel("trip"),
        FieldPanel("author")
    ]

class TripReportCategoryEntryPage(models.Model):
    tripreport = models.ForeignKey(TripReport, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('tripreport', 'category'),)
