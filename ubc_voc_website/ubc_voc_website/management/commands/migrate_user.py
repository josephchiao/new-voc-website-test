from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import pymysql
import os

class Command(BaseCommand):
    help="Migrate Users from old database"

    def handle(self, *args, **options):
        User = get_user_model()

        mysql_conn = pymysql.connect(
            host=os.getenv("OLD_DB_HOST"),
            user=os.getenv("OLD_DB_USER"),
            password=os.getenv("OLD_DB_PASSWORD"),
            database=os.getenv("OLD_DB_DATABASE")
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor
        )

        with mysql_conn.cursor() as cursor:
            cursor.execute("SELECT id, email FROM members;")
            for row in cursor.fetchall():
                user, created = User.objects.get_or_create(
                    email=row['email'],
                    defaults={'old_id': row['id']}
                )
                if created:
                    user.set_password(User.objects.make_random_password())
                    user.save()
                    self.stdout.write(self.style.SUCCESS(f"Created user {user.email}"))
                else:
                    self.stdout.write(f"User {user.email} already exists")

        mysql_conn.close()
        self.stdout.write(self.style.SUCCESS("User migration complete"))