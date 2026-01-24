"""
select id, email from members_table
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string

import csv
from allauth.account.models import EmailAddress

User = get_user_model()

class Command(BaseCommand):
    help="Migrate Users from CSV"

    def handle(self, *args, **options):
        path="user.csv"

        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f, fieldnames=["id", "email"])

            for row in reader:
                user, created = User.objects.get_or_create(
                    email=row['email'].strip(),
                    defaults={
                        'old_id': int(row["id"]),
                        'is_active': True
                    }
                )
                if created:
                    user.set_password(get_random_string(20))
                    user.save()
                    self.stdout.write(self.style.SUCCESS(f"Created user {user.email}"))
                else:
                    self.stdout.write(f"User {user.email} already exists")

                email_obj, email_created = EmailAddress.objects.get_or_create(
                    user=user,
                    email=user.email,
                    defaults={
                        "verified": True,
                        "primary": True
                    }
                )

                if not email_created:
                    email_obj.verified = True
                    email_obj.primary = True
                    email_obj.save()

        self.stdout.write(self.style.SUCCESS("User migration complete"))        