# Generated by Django 3.1.3 on 2021-01-03 12:06

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0016_auto_20210103_0049'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='follows',
            name='followersusers',
        ),
        migrations.AddField(
            model_name='follows',
            name='followersusers',
            field=models.ManyToManyField(related_name='user_followers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='follows',
            name='followingusers',
        ),
        migrations.AddField(
            model_name='follows',
            name='followingusers',
            field=models.ManyToManyField(related_name='user_followings', to=settings.AUTH_USER_MODEL),
        ),
    ]
