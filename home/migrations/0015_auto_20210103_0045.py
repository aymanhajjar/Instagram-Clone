# Generated by Django 3.1.3 on 2021-01-02 22:45

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0014_auto_20210102_2231'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='likers',
        ),
        migrations.AddField(
            model_name='post',
            name='likers',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
