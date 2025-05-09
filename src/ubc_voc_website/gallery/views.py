import os

from django.shortcuts import render
from django.utils.text import slugify

from .forms import UserPhotoUploadForm
from .models import UserGallery

from ubc_voc_website.decorators import Admin, Members, Execs

@Members
def manage_user_gallery(request):
    gallery, created = UserGallery.objects.get_or_create(
        user=request.user,
        defaults={
            'title': f"{request.user.get_full_name()}'s Gallery",
            'is_public': True
        }
    )

    if request.method == 'POST':
        form = UserPhotoUploadForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            photo = form.save(commit=False)

            # Update file path to save in a folder for this user
            _, ext = os.path.splitext(form.cleaned_data['image'].name)
            new_path = f"user/{request.user.id}/{slugify(form.cleaned_data['title'].split(':', 1))}{ext}"
            photo.image.name = new_path

            # Update Photo fields
            photo.caption = f"Photo: {request.user.get_full_name()}"
            photo.slug = slugify(photo.title)
            photo.is_public = True
            photo.save()

            gallery.photos.add(photo)

    else:
        form = UserPhotoUploadForm(user=request.user)

    return render(request, 'gallery/user_gallery.html', {
        'gallery': gallery,
        'form': form
    })

@Members
def create_trip_gallery(request):
    pass

@Members
def add_trip_gallery_photo(request):
    pass
