from django.contrib import admin
from .models import User
from home.models import post, comment, story, follows, profile, notifications
# Register your models here.

admin.site.register(User)
admin.site.register(post)
admin.site.register(comment)
admin.site.register(story)
admin.site.register(follows)
admin.site.register(profile)
admin.site.register(notifications)