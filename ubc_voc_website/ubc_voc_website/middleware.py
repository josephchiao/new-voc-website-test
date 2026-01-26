from django.shortcuts import redirect, render
from django.urls import reverse

from ubc_voc_website.utils import is_member

class MessageBoardMembershipMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/message-board/"):
            if not request.user.is_authenticated:
                return redirect(f"{reverse('account_login')}?next={request.get_full_path()}")
            
            if not is_member(request.user):
                return render(request, "access_denied.html", status=403)
            
        return self.get_response(request)
            