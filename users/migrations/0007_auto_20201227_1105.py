# Generated by Django 3.1.3 on 2020-12-27 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20201227_0206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profilepic',
            field=models.ImageField(blank=True, default='gallery/default.jpg', upload_to='gallery'),
        ),
    ]
