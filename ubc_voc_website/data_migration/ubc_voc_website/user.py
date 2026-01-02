import os
import django
import pymysql

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ubc_voc_website.settings.production")
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

mysql_conn = pymysql.connect(
    host="HOST",
    user="USER",
    password="PASSWORD",
    database="DATABASE",
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

mysql_conn.close()