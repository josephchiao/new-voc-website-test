from django.urls import path, include

from . import views

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.images import urls as wagtailimages_urls
from wagtail import urls as wagtail_urls

urlpatterns = [
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("images", include(wagtailimages_urls)),
    path("create/", views.create_trip_report, name="create_trip_report"),
    path("", include(wagtail_urls))
]