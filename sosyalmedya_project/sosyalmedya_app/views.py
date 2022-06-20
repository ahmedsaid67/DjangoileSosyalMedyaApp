from cmath import log
from operator import ne
import re
from turtle import pos
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages,auth
from .models import Profile,Post,LikePost,FollowersCount
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from itertools import chain
from .forms import UserRegisterForm


@login_required(login_url="signin")
def index(request):
    user_object=User.objects.get(username=request.user.username)
    user_profile=Profile.objects.get(user=user_object)

    user_following_list=[]
    feed=[]
    user_following=FollowersCount.objects.filter(follower=request.user.username)

    for users in user_following:
        user_following_list.append(users.user)

    for usernames in user_following_list:
        feed_lists=Post.objects.filter(user=usernames)
        feed.append(feed_lists)
    
    feed_lists=list(chain(*feed))

    post=Post.objects.all()
    return render(request,"index.html", {"user_profile":user_profile, "posts":feed_lists})

@login_required(login_url="signin")
def upload(request):
    if request.method=="POST":
        user=request.user.username
        image=request.FILES.get('image_upload')
        caption=request.POST["caption"]

        new_post=Post.objects.create(user=user,image=image,caption=caption)
        new_post.save()
        return redirect('/')
    else:
        return redirect('/')

@login_required(login_url="signin")
def search(request):
    username=request.POST["username"]
    username_object=User.objects.filter(username__icontains=username)

    username_profile=[]
    username_profile_list=[]
    for users in username_object:
        username_profile.append(users.id)
        print(users.id)
    
    for ids in username_profile:
        profile_list=Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_list)
        print(profile_list)

    username_profile_list=list(chain(*username_profile_list))


    return render(request,"search2.html", {"username_profile_list":username_profile_list})

@login_required(login_url="signin")
def like_post(request):
    username=request.user.username
    post_id=request.GET.get('post_id')

    post=Post.objects.get(id=post_id)

    like_filter=LikePost.objects.filter(post_id=post_id, username=username).first()

    print(like_filter)
    
    if like_filter == None:
        new_like=LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        return redirect("/")
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect("/")

@login_required(login_url="signin")
def profile(request,pk):
    user_object=User.objects.get(username=pk)
    user_profile=Profile.objects.get(user=user_object)
    user_pots=Post.objects.filter(user=pk)
    user_post_lengt=len(user_pots)

    follower=request.user.username
    user=pk
    if FollowersCount.objects.filter(follower=follower,user=user).first():
        button_text='Unfollow'
    else:
        button_text='Fallow'
        
    user_followers=len(FollowersCount.objects.filter(user=pk))
    user_following=len(FollowersCount.objects.filter(follower=pk))

    context={
        "user_object":user_object,
        "user_profile":user_profile,
        "user_posts":user_pots,
        "user_post_length":user_post_lengt,
        "button_text":button_text,
        "user_followers":user_followers,
        "user_following":user_following,
    }

    return render(request,"profile.html",context)

@login_required(login_url="signin")
def follow(request):
    if request.method=="POST":
        follower=request.POST["follower"]
        user=request.POST["user"]

        if FollowersCount.objects.filter(follower=follower,user=user).first():
            delete_follower=FollowersCount.objects.get(follower=follower,user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower=FollowersCount.objects.create(follower=follower,user=user)
            new_follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect("/")
@login_required(login_url="signin")
def setting(request):
    user_profile=Profile.objects.get(user=request.user)
    if request.method=="POST":
        if request.FILES.get("image")==None:
            image=user_profile.profiloimg
            bio=request.POST["bio"]
            location=request.POST["location"]

            user_profile.profiloimg=image
            user_profile.bio=bio
            user_profile.location=location
            user_profile.save()
        if request.FILES.get("image") !=None:
            image=request.FILES.get("image")
            bio=request.POST["bio"]
            location=request.POST["location"]

            user_profile.profiloimg=image
            user_profile.bio=bio
            user_profile.location=location
            user_profile.save()
        return redirect("setting")
    return render(request,"setting.html",{"user_profile":user_profile})

def signup(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user=authenticate(username=username, password=password)
            login(request, user)
            user_model=User.objects.get(username=username)
            new_profil=Profile.objects.create(user=user_model,id_user=user_model.id)
            new_profil.save()
            messages.success(request, 'Account created ')
            return redirect("/")
    form = UserRegisterForm()
    return render(request, 'signup.html',{'form':form})

def signin(request):
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]
        user_login=authenticate(username=username,password=password)
                
        
        if user_login is not None:
            login(request,user_login)
            return redirect("/")
        else:
            messages.info(request,"Credentials Invalid")
            return redirect('/')
    else:
        return render(request,"signin.html")

    
@login_required(login_url="signin")
def logout_(request):
    logout(request)
    return redirect('signin')