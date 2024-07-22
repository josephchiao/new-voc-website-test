from django.shortcuts import render, get_object_or_404
from django.db.models import OuterRef, Subquery
from django.contrib.auth import get_user_model
from .models import Exec, Membership, Profile
from ubc_voc_website.decorators import Members, Execs

@Members
def member_list(request):
    members = Profile.objects.all().filter(user__is_active=True)
    return render(request, 'membership/members.html', {'members': members})

@Members
def profile(request, id):
    user = get_object_or_404(get_user_model(), id=id)
    profile = Profile.objects.get(user=user)
    return render(request, 'membership/profile.html', {'user': user, 'profile': profile})

@Members
def my_profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    return render(request, 'membership/profile.html', {'user': user, 'profile': profile})

@Execs
def edit_user_profile(request, id):
    user = get_object_or_404(get_user_model(), id=id)
    profile = Profile.objects.get(user=user)
    return render(request, 'membership/profile.html', {'user': user, 'profile': profile})

@Execs
def manage_roles(request): # not sure what i had in mind for this one but i'll sort it out later
    execs = Exec.objects.filter(user=OuterRef('user'))
    users = Profile.objects.all().filter(user__in=Subquery(execs.values('user')))
    return render(request, 'membership/manage_roles.html', {'execs': execs, 'users': users})

@Execs
def membership_stats(request):
    num_inactive_accounts = Profile.objects.all().filter(user__is_active=False).count()
    num_regular_members = Membership.objects.all().filter(type=Membership.MembershipType.REGULAR).count()
    num_associate_members = Membership.objects.all().filter(type=Membership.MembershipType.ASSOCIATE).count()
    num_honourary_members = Membership.objects.all().filter(type=Membership.MembershipType.HONORARY).count()
    return render(request, 'membership/membership_stats.html', {
         'num_inactive_accounts': num_inactive_accounts, 
         'num_regular_members': num_regular_members, 
         'num_associate_members': num_associate_members, 
         'num_honourary_members': num_honourary_members
        })
    
    # TODO add more stats that would be useful/interesting (trip signups, etc.)
