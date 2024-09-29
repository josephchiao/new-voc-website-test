from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .models import Exec, Membership, Profile
from ubc_voc_website.decorators import Members, Execs
from .forms import MembershipForm, ProfileForm, WaiverForm
from django.http import HttpResponseForbidden
from django.core.files.base import ContentFile

import base64

@login_required
def apply(request):
    if request.method == 'POST':
        form = MembershipForm(request.POST, user=request.user)
        if form.is_valid():
            membership = form.save()
            return redirect(f'waiver/{membership.id}')
    else:
        form = MembershipForm(user=request.user)
    return render(request, 'membership/apply.html', {'form': form})

@login_required
def waiver(request, membership_id):
    membership = get_object_or_404(Membership, id=membership_id)
    if membership.user != request.user:
        return HttpResponseForbidden()
    
    if request.method == "POST":
        form = WaiverForm(request.POST, user=request.user)
        if form.is_valid():
            waiver = form.save(commit=False)
            waiver.membership = membership
            signature_data = request.POST['signature']

            f, imgstr = signature_data.split(';base64')
            data = ContentFile(base64.base64decode(imgstr))

            waiver.signature.save('signature.png', data, save=False)

            waiver = form.save()
            return redirect('home')
        
    else:
        form = WaiverForm(user=request.user)

    return render(request, 'membership/waiver.html', {'form': form})

@Members
def member_list(request):
    members = Profile.objects.all().filter(user__is_active=True)
    return render(request, 'membership/members.html', {'members': list(members)})

@Members
def profile(request, id):
    user = get_object_or_404(get_user_model(), id=id)
    profile = Profile.objects.get(user=user)
    return render(request, 'membership/profile.html', {'user': user, 'profile': profile})

@Members
def edit_profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect(f'profile/{user.id}')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'membership/edit_profile.html', {'form': form})

@Execs
def manage_roles(request): # for managing who has the exec role
    exec_group, created = Group.objects.get_or_create(name='Exec')

    if request.method == "POST":
        user_id = request.POST.get('member')
        exec_role = request.POST.get('position')

        try:
            User = get_user_model()
            user = get_object_or_404(User, id=user_id)
            profile = get_object_or_404(Profile, user=user)

            if Exec.objects.filter(user=user).exists():
                messages.error(request, f"{profile.first_name} {profile.last_name} already has an exec position")
            else:
                exec = Exec.objects.create(user=user, exec_role=exec_role)
                exec.save()

                exec_group.user_set.add(user)

                messages.success(request, f"{profile.first_name} {profile.last_name} has been added to Exec with the role {exec_role}")

        except User.DoesNotExist:
            messages.error(request, "Selected user does not exist")

        return redirect('manage_roles')

    else:
        # Ignore anyone who has somehow ended up with an entry in the exec table without the group role, although this should (hopefully) never happen
        execs = Exec.objects.filter(user__groups__id=exec_group.id)

        execs_extended_info = []

        for exec in execs:
            profile = Profile.objects.get(user=exec.user)
            execs_extended_info.append({
                'id': exec.user.id,
                'role': exec.exec_role,
                'first_name': profile.first_name,
                'last_name': profile.last_name
            })

        non_execs = Profile.objects.exclude(user__groups=exec_group)
        non_execs_extended_info = []

        for profile in non_execs:
            non_execs_extended_info.append({
                'id': profile.user.id,
                'first_name': profile.first_name,
                'last_name': profile.last_name
            })

        return render(request, 'membership/manage_roles.html', {'execs': execs_extended_info, 'members': non_execs_extended_info})

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
