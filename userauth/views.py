from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from post.models import Post, Follow, Stream
from .models import Profile
from .forms import EditProfileForm, UserRegistrationForm
from django.core.paginator import Paginator
from django.urls import resolve
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate
from django.db.models import Q

# Create your views here.
@login_required
def userProfile(request, username):
    user= get_object_or_404(User, username= username)
    profile= Profile.objects.get(user= user)
    url_name= resolve(request.path).url_name
    if url_name== 'profile':
        posts= Post.objects.filter(user= user).order_by('-posted')
    else:
        posts= profile.favourite.all()

    # Track number of posts and followers, following
    post_count= Post.objects.filter(user= user).count()
    following_count= Follow.objects.filter(follower= user).count()
    followers_count= Follow.objects.filter(following= user).count()

    # Follow status
    follow_status= Follow.objects.filter(follower= request.user , following= user).exists()
    
    # pagination
    # paginator= Paginator(posts, 9)
    # page_number= request.GET.get('page')
    # posts_paginator= paginator.get_page(page_number)

    context={
        # 'post_paginator': posts_paginator,
        'posts': posts,
        'profile': profile,
        'url_name': url_name,
        'post_count': post_count,
        'following_count': following_count,
        'followers_count': followers_count,
        'follow_status': follow_status
    }
    return render(request, 'profile.html', context)

@login_required
def follow(request, username):
    user= request.user
    following= get_object_or_404(User, username= username)
    try:
        followed= Follow.objects.filter(follower= user , following= following).exists()

        if not followed:
            followed= Follow.objects.create(follower= user, following= following)
            posts= Post.objects.filter(user= following)[:5]       #5 posts which are already posted by the user, are added in stream of follower
            with transaction.atomic():
                for post in posts:
                    stream= Stream(post=post, user= user, date= post.posted, following= following)
                    stream.save()
        else:
            followed= Follow.objects.filter(follower= user, following= following).delete()
            Stream.objects.filter(user= user, following= following).all().delete()
 
        return HttpResponseRedirect(reverse('profile', args= [username]))
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('profile', args= [username]))
    
@login_required
def editProfile(request, username):
    user= request.user
    profile= get_object_or_404(Profile, user= user)
    if request.method== 'POST':
        form= EditProfileForm(request.POST, request.FILES, instance= profile)
        if form.is_valid():
            form.save()
            return  HttpResponseRedirect(reverse('profile', args= [username]))
    else:
        form= EditProfileForm(instance= profile)
    return render(request, 'editprofile.html', {'form': form})

def register(request):
    if request.method== 'POST':
        form= UserRegistrationForm(request.POST)
        if form.is_valid():
            user= form.save(commit=False)
            user.first_name= form.cleaned_data['first_name']
            user.last_name= form.cleaned_data['last_name']
            user.set_password(form.cleaned_data['password1'])
            user.username= form.cleaned_data['username']
            user.save()
            Profile.objects.create(user= user, first_name= user.first_name, last_name= user.last_name)
            login(request, user)
            return redirect('index')
    
    elif request.user.is_authenticated:
        return redirect('index')

    else:
        form= UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def searchUser(request):
    query= request.GET.get('q','')
    if query:
        search_users= User.objects.filter(Q(profile__first_name__icontains= query) | Q(profile__last_name__icontains= query))
    else:
        search_users = User.objects.none()
    
    paginator = Paginator(search_users, 10)     # Create a Paginator object with 10 searched users per page
    page_number = request.GET.get('page')       # Get the page number from the GET parameters
    page_obj = paginator.get_page(page_number)  # Retrieve the corresponding page of items
    
    return render(request, 'searchUser.html', {'search_results': page_obj})