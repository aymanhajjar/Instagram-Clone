# Generated by Django 3.1.3 on 2021-01-02 12:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0010_post_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='saved_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users_saved', to=settings.AUTH_USER_MODEL),
        ),
    ]
