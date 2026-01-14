from django.http import JsonResponse
from django.shortcuts import render

from ubc_voc_website.decorators import MembersAPI
from ubc_voc_website.utils import is_exec

from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import AccessToken


PHOTO_CONTEST_ALBUM = "photo-contest-2025"

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

@api_view(["POST"])
@MembersAPI
def wp_sso_token(request):
    token = AccessToken.for_user(request.user)

    token["email"] = request.user.email
    token["first_name"] = request.user.profile.first_name
    token["last_name"] = request.user.profile.last_name
    token["member"] = True

    if request.user.is_superuser or request.user.is_staff:
        token["wp_role"] = "administrator"
    elif is_exec(request.user):
        token["wp_role"] = "editor"
    else:
        token["wp_role"] = "author"

    return JsonResponse({
        "token": str(token)
    })