# Generated by Django 3.1.3 on 2021-01-02 12:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_auto_20210102_0017'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='userprofile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='post_profile', to='home.profile'),
        ),
    ]
