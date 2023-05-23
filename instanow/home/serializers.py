from .models import post
from users.models import User
from rest_framework import serializers
from django.core import serializers

seriallikers = serializers.serialize('json', [post.likers,])