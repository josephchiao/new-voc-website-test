from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from membership.models import Profile

class MembershipViewTests(TestCase):
    def setUp(self):
        self.members = Group.objects.create(name='Members')
        self.exec = Group.objects.create(name='Exec')

        self.User = get_user_model()
        self.non_member = self.User.objects.create_user(
            email='notavocer@notubcvoc.com',
            password='iamnotinthevoc'
        )
        self.non_member_profile = Profile.objects.create(
            user=self.non_member,
            first_name='Test',
            last_name='User',
            phone='(111)-111-1111'
        )
        
        self.member = self.User.objects.create_user(
            email='vocer@gmail.com',
            password='iaminthevoc'
        )
        self.member.groups.add(self.members)
        self.member_profile = Profile.objects.create(
            user=self.member,
            first_name='Test2',
            last_name='User2',
            phone='(222)-222-2222'
        )

        self.exec_member = self.User.objects.create_user(
            email='vocexec@gmail.com',
            password='iamonexec'
        )
        self.exec_member.groups.add(self.members, self.exec)
        self.exec_member_profile = Profile.objects.create(
            user=self.exec_member,
            first_name='Test3',
            last_name='User3',
            phone='(333)-333-3333'
        )

    def test_members(self):
        self.client.login(username='notavocer@notubcvoc.com', password='iamnotinthevoc')
        response = self.client.get(reverse('members'))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateNotUsed(response, 'membership/members.html')

        self.client.login(username='vocer@gmail.com', password='iaminthevoc')
        response = self.client.get(reverse('members'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'membership/members.html')

        self.client.login(username='vocexec@gmail.com', password='iamonexec')
        response = self.client.get(reverse('members'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'membership/members.html')

    def test_profile(self):
        self.client.login(username='notavocer@notubcvoc.com', password='iamnotinthevoc')
        response = self.client.get(reverse('profile', args=[self.member.id]))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateNotUsed(response, 'membership/profile.html')

        self.client.login(username='vocer@gmail.com', password='iaminthevoc')
        response = self.client.get(reverse('profile', args=[self.member.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'membership/profile.html')

        self.client.login(username='vocexec@gmail.com', password='iamonexec')
        response = self.client.get(reverse('profile', args=[self.member.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'membership/profile.html')

    def test_my_profile(self):
        self.client.login(username='notavocer@notubcvoc.com', password='iamnotinthevoc')
        response = self.client.get(reverse('my_profile'))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateNotUsed(response, 'membership/profile.html')

        self.client.login(username='vocer@gmail.com', password='iaminthevoc')
        response = self.client.get(reverse('my_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'membership/profile.html')

        self.client.login(username='vocexec@gmail.com', password='iamonexec')
        response = self.client.get(reverse('my_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'membership/profile.html')

    def test_edit_user_profile(self):
        self.client.login(username='notavocer@notubcvoc.com', password='iamnotinthevoc')
        response = self.client.get(reverse(f'edit_user_profile', args=[self.member.id]))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateNotUsed(response, 'membership/profile.html')

        self.client.login(username='vocer@gmail.com', password='iaminthevoc')
        response = self.client.get(reverse(f'edit_user_profile', args=[self.member.id]))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateNotUsed(response, 'membership/profile.html')

        self.client.login(username='vocexec@gmail.com', password='iamonexec')
        response = self.client.get(reverse(f'edit_user_profile', args=[self.member.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'membership/profile.html')

    def test_manage_roles(self):
        self.client.login(username='notavocer@notubcvoc.com', password='iamnotinthevoc')
        response = self.client.get(reverse('manage_roles'))
        self.assertEqual(response.status_code, 403)

        self.client.login(username='vocer@gmail.com', password='iaminthevoc')
        response = self.client.get(reverse('manage_roles'))
        self.assertEqual(response.status_code, 403)

        self.client.login(username='vocexec@gmail.com', password='iamonexec')
        response = self.client.get(reverse('manage_roles'))
        self.assertEqual(response.status_code, 200)

    def test_membership_stats(self):
        self.client.login(username='notavocer@notubcvoc.com', password='iamnotinthevoc')
        response = self.client.get(reverse('membership_stats'))
        self.assertEqual(response.status_code, 403)

        self.client.login(username='vocer@gmail.com', password='iaminthevoc')
        response = self.client.get(reverse('membership_stats'))
        self.assertEqual(response.status_code, 403)

        self.client.login(username='vocexec@gmail.com', password='iamonexec')
        response = self.client.get(reverse('membership_stats'))
        self.assertEqual(response.status_code, 200)