from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.models import User
from django.core.paginator import Paginator
from .models import post, comment, story, profile, follows, seriallikers, notifications, serialpost, serialfollows, serialsearch
import json as simplejson
from django.http import Http404
from django.core import serializers
import random
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.

@login_required(login_url='login/')
def homepage(request):
    thisuser = User.objects.get(username=request.user.username)

    followedprofiles = profile.objects.filter(followersusers=thisuser)

    userinfo = profile.objects.get(owner=thisuser)

    notf = notifications.objects.filter(owner=thisuser).order_by('-date')

    if followedprofiles.count()==0:
        followedusers = False
        thereareposts = False

        return render (request, "homeposts.html", {
        "thisuser": thisuser,
        "followedusers": followedusers,
        "thisuserinfo": userinfo,
        "notf": notf,
        "thereareposts": thereareposts
    })
    else:
        thereareposts = True
        followeduser = followedprofiles[0].owner
        userposts = post.objects.filter(author=followeduser).order_by('-id')[:50]
        for i in range(1,followedprofiles.count()):
            followedusers = followedprofiles[i].owner
            userposts |= post.objects.filter(author=followedusers).order_by('-id')[:50]
        orderedposts = userposts.order_by('-date_posted')

        paginator = Paginator(orderedposts, per_page=5)
        page_num = int(request.GET.get("page", 1))
        if page_num > paginator.num_pages:
            raise Http404
        posts = paginator.page(page_num)
        if is_ajax(request):
            return render(request, '_homeposts.html', {'posts': posts})
        
        
        return render (request, "homeposts.html", {
        "thisuser": thisuser,
        "followedusers": followedusers,
        "followedposts": posts,
        "thisuserinfo": userinfo,
        "notf": notf,
        "thereareposts": thereareposts
    })

def userprofile(request, username):
    if request.method == 'GET':
        visitinguser = User.objects.get(username=request.user.username)
        thisuser = User.objects.get(username=username)
        thisuserinfo = profile.objects.get(owner=visitinguser)
        notf = notifications.objects.filter(owner=visitinguser).order_by('-date')

        userposts = post.objects.filter(author=thisuser)
        paginator = Paginator(userposts, per_page=5)
        page_num = int(request.GET.get("page", 1))
        if page_num > paginator.num_pages:
            raise Http404
        posts = paginator.page(page_num)
        if is_ajax(request):
            return render(request, '_post.html', {'posts': posts})

        
        userstories = story.objects.filter(author=thisuser)
        userinfo = profile.objects.get(owner=thisuser)
        followers = follows.objects.filter(mainuser=thisuser)
        following = follows.objects.filter(mainuser=thisuser)
        followercount = userinfo.followercount
        followingcount = userinfo.followingcount
        postcount = post.objects.filter(author=thisuser).count()

        profileowner = User.objects.get(username=username)
        tagged_posts = post.objects.filter(tagged_users=profileowner)
        tagged_posts_count = tagged_posts.count()

        if visitinguser in userinfo.followersusers.all():
            followed = True
        else:
            followed = False

        svdposts = post.objects.filter(saved_by=profileowner)
        svdposts_count = svdposts.count()


        return render (request, "profile.html", {
            "owner": thisuser,
            "userposts": posts,
            "userstories": userstories,
            "userinfo": userinfo,
            "postcount": postcount,
            "followers": followers,
            "following": following,
            "followercount": followercount,
            "taggedposts": tagged_posts,
            "followingcount": followingcount,
            "savedposts": svdposts,
            "tagged_posts_count": tagged_posts_count,
            "svdposts_count": svdposts_count,
            "followed": followed,
            "notf": notf,
            "thisuserinfo": thisuserinfo
        })

@login_required(login_url='login/')
def editprofile(request, username):
    thisuser = User.objects.get(username=username)
    userinfo = profile.objects.get(owner=thisuser)
    notf = notifications.objects.filter(owner=thisuser).order_by('-date')
    if request.method == "GET":
        thisuser = User.objects.get(username=username)
        if request.user != thisuser:
            raise Http404

        userinfo = profile.objects.get(owner=thisuser)

        return render(request, "settings.html", {
            "thisuser": thisuser,
            "userinfo": userinfo,
            "thisuserinfo": userinfo,
            "notf": notf
        })

    elif request.method == 'POST':
        name = request.POST['name']
        username = request.POST['username']
        website = request.POST['website']
        bio = request.POST['bio']
        email = request.POST['email']
        ppic = request.FILES['updatepic'] if 'updatepic' in request.FILES else False

        if len(name)>20:
            return render(request, "settings.html", {
        "thisuser": thisuser,
        "userinfo": userinfo,
        "namemsg": 'This name is too long choose a shorter one!',
        "thisuserinfo": userinfo,
        "notf": notf
    })

        if len(username)>20:
           return render(request, "settings.html", {
        "thisuser": thisuser,
        "userinfo": userinfo,
        "usermsg": 'This username is too long choose a shorter one!',
        "thisuserinfo": userinfo,
        "notf": notf
    }) 

        if username == request.user.username:
            pass
        elif len(User.objects.filter(username=username)) > 0:
           return render(request, "settings.html", {
        "thisuser": thisuser,
        "userinfo": userinfo,
        "usermsg": 'This username is already taken, please choose another one!',
        "thisuserinfo": userinfo,
        "notf": notf
    })  

        if len(website)>50:
            return render(request, "settings.html", {
        "thisuser": thisuser,
        "userinfo": userinfo,
        "linkmsg": 'Your website URL cannot be this long!',
        "thisuserinfo": userinfo,
        "notf": notf
    })  

        if len(bio)>150:
           return render(request, "settings.html", {
        "thisuser": thisuser,
        "userinfo": userinfo,
        "biomsg": 'Your bio is too long!',
        "thisuserinfo": userinfo,
        "notf": notf
    })   

        if len(email)>30:
           return render(request, "settings.html", {
        "thisuser": thisuser,
        "userinfo": userinfo,
        "emailmsg": 'Please enter a valid email address',
        "thisuserinfo": userinfo,
        "notf": notf
    })   

        if ppic:
            if ppic.size > 5242880:
                return render(request, "settings.html", {
            "thisuser": thisuser,
            "userinfo": userinfo,
            "picmsg": 'Your picture cannot be bigger than 5MB!',
            "thisuserinfo": userinfo,
            "notf": notf
        })   

    userinfo = profile.objects.get(owner=thisuser)
    userinfo.Name = name
    userinfo.link = website
    userinfo.bio = bio
    userinfo.email = email
    if ppic:
        userinfo.profilepic = ppic
    userinfo.save()
    thisuser.username = username
    thisuser.save()

    return render (request, "settings.html", {
        "thisuser": thisuser,
        "thisuserinfo": userinfo,
        "userinfo": userinfo,
        "successmsg": 'Updated Successfully!'
    })   

def postdetails(request, postid):

    postclicked = post.objects.get(id=postid)
    postinfo = serialpost(postclicked)

    if request.method == "GET":
            return JsonResponse(postinfo.data)

def postlikers(request, postid):
    likedpost = post.objects.get(id=postid)
    likerslist = likedpost.likers.all()
    likers = seriallikers(likerslist, many=True)
    return JsonResponse(likers.data, safe=False)

            
def taggedposts(request, username):
    
    profileowner = User.objects.get(username=username)
    tagged_posts = post.objects.filter(tagged_users=profileowner)
    return JsonResponse([post.serialize() for post in tagged_posts], safe=False)

@login_required(login_url='login/')
def savedposts(request):
    pass

def is_ajax(request):
    """
    This utility function is used, as `request.is_ajax()` is deprecated.

    This implements the previous functionality. Note that you need to
    attach this header manually if using fetch.
    """
    return request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"

@login_required(login_url='login/')
def likepost(request, postid):
    thispost = post.objects.get(id=postid)
    thisuser = request.user
    thisuserprof = profile.objects.get(owner=thisuser)
    likinguser = request.user
    thispost.likers.add(likinguser)
    thispost.like_count = thispost.like_count + 1
    thispost.save()
    postowner = thispost.author
    text = thisuser.username + ' liked your post!'
    newnotf = notifications.objects.create(owner=postowner, text=text, post=thispost, triggeredby=thisuserprof)
    newnotf.save()
    return JsonResponse(thispost.serialize())

@login_required(login_url='login/')
def unlikepost(request, postid):
    thispost = post.objects.get(id=postid)
    likinguser = request.user
    thispost.likers.remove(likinguser)
    thispost.like_count = thispost.like_count - 1
    thispost.save()
    return JsonResponse(thispost.serialize())

@login_required(login_url='login/')
def addcomment(request, postid):
    thispost = post.objects.get(id=postid)
    thisuser = request.user
    thisuserprof = profile.objects.get(owner=thisuser)
    commenttext = request.POST['commenttext']
    newcomment = comment.objects.create(post=thispost, author=thisuser, text=commenttext)
    newcomment.save()
    thispost.comment_count = thispost.comment_count + 1
    thispost.save()
    postowner = thispost.author
    text = thisuser.username + ' left a comment on your post!'
    newnotf = notifications.objects.create(owner=postowner, text=text, post=thispost, triggeredby=thisuserprof)
    newnotf.save()
    return JsonResponse(newcomment.serialize())

@login_required(login_url='login/')
def savepost(request, postid):
    thispost = post.objects.get(id=postid)
    savinguser = request.user
    thispost.saved_by.add(savinguser)
    return JsonResponse(thispost.serialize())

@login_required(login_url='login/')
def unsavepost(request, postid):
    thispost = post.objects.get(id=postid)
    savinguser = request.user
    thispost.saved_by.remove(savinguser)
    return JsonResponse(thispost.serialize())

def explore(request):
    allposts = post.objects.all().order_by('?')[:100]

    paginator = Paginator(allposts, per_page=9)
    page_num = int(request.GET.get("page", 1))
    if page_num > paginator.num_pages:
        raise Http404
    posts = paginator.page(page_num)
    if is_ajax(request):
        return render(request, '_post.html', {'posts': posts})

    userprof = profile.objects.get(owner=request.user)
    notf = notifications.objects.filter(owner=request.user).order_by('-date')

    return render(request, "explore.html", {
        "randomposts": posts,
        "thisuserinfo": userprof,
        "notf": notf
    })

@login_required(login_url='login/')   
def follow(request, targetuser):
    targetus = User.objects.get(username=targetuser)
    targetuserprofile = profile.objects.get(owner=targetus)
    thisuserusername = request.POST['thisuser']
    thisuser = User.objects.get(username=thisuserusername)
    targetuserprofile.followersusers.add(thisuser)
    targetuserprofile.followercount = targetuserprofile.followercount + 1
    targetuserprofile.save()
    thisuserprofile = profile.objects.get(owner=thisuser)
    thisuserprofile.followingusers.add(targetus)
    thisuserprofile.followingcount = thisuserprofile.followingcount + 1
    thisuserprofile.save()
    serialprof = serialfollows(targetuserprofile)
    return JsonResponse(serialprof.data, safe=False)

@login_required(login_url='login/')
def unfollow(request, targetuser):
    targetus = User.objects.get(username=targetuser)
    targetuserprofile = profile.objects.get(owner=targetus)
    thisuserusername = request.POST['thisuser']
    thisuser = User.objects.get(username=thisuserusername)
    targetuserprofile.followersusers.remove(thisuser)
    targetuserprofile.followercount = targetuserprofile.followercount -1
    targetuserprofile.save()
    thisuserprofile = profile.objects.get(owner=thisuser)
    thisuserprofile.followingusers.remove(targetus)
    thisuserprofile.followingcount = thisuserprofile.followingcount -1
    thisuserprofile.save()
    serialprof = serialfollows(targetuserprofile)
    return JsonResponse(serialprof.data, safe=False)

def search(request, query):
    thisquery = query
    userquery = User.objects.filter(username__startswith=thisquery)
    results = []
    for u in userquery:
        uprof = profile.objects.get(owner = u)
        results.append(uprof)
    resultsserial = serialsearch(results, many=True)
    return JsonResponse(resultsserial.data, safe=False)

@login_required(login_url='login/')
def newpost(request):
    thisuser= request.user
    thisuserinfo = profile.objects.get(owner=thisuser)
    notf = notifications.objects.filter(owner=request.user).order_by('-date')
    userprofs = profile.objects.all()

    if request.method == "GET":
        
        return render(request, "create.html", {
            "thisuserinfo": thisuserinfo,
            "notf": notf,
            "userprofs": userprofs
        })
    if request.method == "POST":

        image = request.FILES['postpic'] if 'postpic' in request.FILES else False
        caption = request.POST['formcaption']
        tagged = request.POST['tagged']
        if tagged != '':
            taggeduser = User.objects.get(username=tagged)
        else: 
            taggeduser = None

        if image == False:
            return render(request, "create.html", {
                "thisuserinfo": thisuserinfo,
                "notf": notf,
                "userprofs": userprofs,
                "imgmsg": 'Please choose an image!'
            })
        
        if tagged != '':
            createdpost = post.objects.create(author=thisuser, image=image, caption=caption, userprofile=thisuserinfo)
            createdpost.tagged_users.set(taggeduser)
            createdpost.save()
        else:
            createdpost = post.objects.create(author=thisuser, image=image, caption=caption, userprofile=thisuserinfo)
            createdpost.save()
        return render(request, "create.html", {
                "thisuserinfo": thisuserinfo,
                "notf": notf,
                "userprofs": userprofs,
                "msg": 'Success!'
            })
        
