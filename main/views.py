from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_text
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout

from main.forms import SignUpForm,PostForm
from main.tokens import account_activation_token
from .models import *

import datetime
import time

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.

# Home page
def index(request):
    if request.user.is_authenticated:
        is_guest = 0
    else:
        is_guest = 1

    return render(request,"main/index.html",{
        "users": User.objects.all(),
        "posts": Post.objects.all().order_by('-date'),
        "is_guest": is_guest
    })

# Sign up page
def signup(request):
    # If the form had errors or something resubmit
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your Network Account'
            message = render_to_string('user/accountactivation.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return HttpResponseRedirect(reverse("user:account_activation_sent"))
    else:
        form = SignUpForm()
    # If you're visiting normally return a blank form
    return render(request, "main/signup.html", {'form': form})



def login_view(request,liking=0):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if liking == 1:
            return render(request, "main/login.html", {
                "message": "Log in to like a post."
            })
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("main:index"))
        else:
            return render(request, "main/login.html", {
                "message": "Invalid credentials."
            })
    return render(request, "main/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("main:index"))

def newpost_view(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        form.instance.owner = request.user
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("main:index"))
    else:
        form = PostForm()
    return render(request, "main/newpost.html", {'form': form})

def newcomment_view(request):
    if request.method == "POST":
        text = request.POST.get("text")
        owner = request.user
        post = Post.objects.get(pk=request.POST.get("post"))
        c = Comment.objects.create_comment(post,owner,text)
        c.save()
        return HttpResponseRedirect(reverse("main:index"))
    else:
        return render(request, "main/index.html")

def deletecomment_view(request):
    if request.method == "POST":
        Comment.objects.get(pk=request.POST.get("comment")).delete()
        return HttpResponseRedirect(reverse("main:index"))
    else:
        return render(request, "main/index.html")

def deletepost_view(request):
    if request.method == "POST":
        Post.objects.get(pk=request.POST.get("post")).delete()
        return HttpResponseRedirect(reverse("main:index"))
    else:
        return render(request, "main/index.html")

def follow_view(request):
    if request.method == "POST":
        if request.POST.get("f") == "0":
            person = User.objects.filter(id=request.POST.get("person")).get()
            person.followers.add(request.user)
            return HttpResponseRedirect(reverse("main:userpage",kwargs={'name':person.username}))
        else:
            person = User.objects.filter(id=request.POST.get("person")).get()
            person.followers.remove(request.user)
            return HttpResponseRedirect(reverse("main:userpage",kwargs={'name':person.username}))
    else:
        return render(request, "main/index.html")

def userpage(request,name):

    try:
        pageuser = User.objects.get(username=name)
        message = 0
        posts = Post.objects.all().filter(owner=pageuser).order_by('-date')

        if request.user.is_authenticated:
            is_guest = 0
            if pageuser in request.user.following.all():
                is_following = 1
            else: 
                is_following = 0
        else:
            is_guest = 1
            is_following = 0
        
    except Exception:
        if request.user.is_authenticated:
            is_guest = 0
        else:
            is_guest = 1
        is_following = 0
        
        pageuser = None
        posts = None
        message = 1

    

    return render(request,"main/userpage.html",{
        "is_guest" : is_guest,
        "pageuser" : pageuser,
        "message" : message,
        "users" : User.objects.all(),
        "posts" : posts,
        "is_following" : is_following
    })