# Generated by Django 3.1.3 on 2021-01-03 18:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0020_notifications'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='postnotf', to='home.post'),
        ),
    ]