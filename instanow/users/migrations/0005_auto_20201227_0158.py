# Generated by Django 3.1.3 on 2020-12-26 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_profilepic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profilepic',
            field=models.ImageField(blank=True, upload_to='gallery'),
        ),
    ]
