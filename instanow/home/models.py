from django.db import models
from django.utils import timezone
from django.contrib.humanize.templatetags import humanize
from users.models import User
from django.core import serializers
from rest_framework import serializers


# Create your models here.

class profile(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_prof")
    Name = models.CharField(max_length=50, blank=True,)
    bio = models.TextField(max_length=1000, default="")
    email = models.EmailField(blank=True)
    link = models.URLField(max_length=50, blank=True)
    followercount = models.IntegerField(default=0)
    followingcount = models.IntegerField(default=0)
    followersusers = models.ManyToManyField(User, related_name="user_follower", blank=True)
    followingusers = models.ManyToManyField(User, related_name="user_following", blank=True)
    profilepic = models.ImageField(upload_to='gallery', default="gallery/default.jpg", blank=True)

    def __str__(self):
        return self.owner.username

class serialfollows(serializers.ModelSerializer):

    class Meta:
        model = profile
        fields =('followercount', 'followingcount')

class serialprofilepic(serializers.ModelSerializer):
    ppic = serializers.CharField(source='profilepic')
    class Meta:
        model = profile
        fields =('ppic',)

class serialsearch(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    ppic = serializers.CharField(source='profilepic')

    class Meta:
        model = profile
        fields = ('username', 'ppic')

    def get_username(self, instance):
        uname = instance.owner.username
        return uname

class post(models.Model):
    image = models.ImageField(blank = True)
    video = models.FileField(upload_to='post_videos', blank = True)
    caption = models.TextField(max_length=3000, blank=True, default="")
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_posts")      #to prevent user from being deleted when post is deleted
    comment_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    likers = models.ManyToManyField(User, related_name="liked_posts", blank=True)
    tagged_users = models.ManyToManyField(User, related_name="taggedin", blank=True)
    saved_by = models.ManyToManyField(User, related_name="saved_posts", blank=True)
    userprofile = models.ForeignKey(profile, on_delete=models.CASCADE, related_name="post_profile", null=True)

    def __str__(self):
        return self.caption + ' by ' + self.author.username

    def get_date_posted(self):
        return humanize.naturaltime(self.date_posted)

    if tagged_users:
        def serialize(self):
            return {
                "image": self.image.url,
                "caption": self.caption,
                "date": self.date_posted,
                "owner": self.author.username,
                "commentcount": self.comment_count,
                "likecount": self.like_count,
                "taggedusers": None
            }


        
    else:
        def serialize(self):
            return {
                "image": self.image.url,
                "caption": self.caption,
                "date": self.date_posted,
                "owner": self.author.username,
                "commentcount": self.comment_count,
                "likecount": self.like_count,
            }

class seriallikers(serializers.ModelSerializer):
    liker = serializers.CharField(source='username')
    profileimage = serializers.SerializerMethodField()

    class Meta:
        model = post
        fields = ('liker', 'profileimage')

    def get_profileimage(self, instance):
        profimg = instance.user_prof.get().profilepic.url
        return profimg

class serialsaved(serializers.ModelSerializer):
    saver = serializers.CharField(source='username')

    class Meta:
        model = post
        fields = ('saver',)

class serialpost(serializers.ModelSerializer):
    liker = serializers.SerializerMethodField()
    profileimage = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    savedby = serializers.SerializerMethodField()

    class Meta:
        model = post
        fields = '__all__'

    def get_profileimage(self, instance):
        profimg = instance.userprofile.profilepic.url
        return profimg
    def get_liker(self, instance):
        like = instance.likers.all()
        likes = seriallikers(like, many=True)
        return likes.data
    def get_username(self, instance):
        usern = instance.author.username
        return usern
    def get_comments(self, instance):
        pcomment = instance.comments.all()
        postcomments = serialcomment(pcomment, many=True)
        return postcomments.data
    def get_savedby(self, instance):
        svdby = instance.saved_by.all()
        svdbysl = serialsaved(svdby, many=True)
        return svdbysl.data


class story(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_stories")
    views = models.IntegerField(default='0')
    viewers = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_viewers")
    image = models.ImageField()


class comment(models.Model):
    post = models.ForeignKey(post, on_delete=models.CASCADE, related_name="comments", null=True)
    text = models.TextField(max_length=800)
    date_created = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")

    def get_date_created(self):
        return humanize.naturaltime(self.date_created)
    
    def __str__(self):
        return self.text

    def serialize(self):
        return {
            "owner": self.author.username,
            "post": self.post.id,
            "date": self.date_created,
            "text": self.text,
            "commentcount": self.post.comment_count
        }    

class follows(models.Model):
    mainuser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_ref")
    followersusers = models.ManyToManyField(User, related_name="user_followers", blank=True)
    followingusers = models.ManyToManyField(User, related_name="user_followings", blank=True)


class notifications(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    text = models.TextField(default="")
    date = models.DateTimeField(default=timezone.now)
    read = models.BooleanField(default=False)
    triggeredby = models.ForeignKey(profile, on_delete=models.CASCADE, related_name="sentnotf", null=True)
    post = models.ForeignKey(post, on_delete=models.CASCADE, related_name="postnotf", null=True)

    def __str__(self):
        return self.text + ' for ' + self.owner.username

class serialcomment(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    userpic = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()

    class Meta:
        model = comment
        fields = '__all__'

    def get_username(self, instance):
        username = instance.author.username
        return username
    def get_userpic(self, instance):
        upic = instance.author.user_prof.all()
        uspic = serialprofilepic(upic, many=True)
        return uspic.data
    def get_date(self, instance):
        datecreated = instance.get_date_created()
        return datecreated