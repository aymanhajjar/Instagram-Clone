# Generated by Django 3.1.3 on 2020-12-26 16:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_fullname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='fullname',
        ),
    ]