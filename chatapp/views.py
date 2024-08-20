from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message
from userauth.models import Profile
from .forms import SendMessageForm
from django.db.models import Q
from django.core.paginator import Paginator

@login_required
def inbox(request):
    user= request.user
    messages= Message.get_message(user= user)      #fetch the user's messages, grouped by recipient, including the last message date and unread count    
    
    return render(request, 'chatapp/inbox.html', {'messages': messages})

@login_required   
def directs(request, username):
    user= request.user
    messages= Message.get_message(user=user)
    active_direct= username     #active_directs represent the username of the user with whom the most recent conversation is active
    directs= Message.objects.filter(user= user, reciepient__username= active_direct)     #store the list of messages exchanged between the logged-in user and the active direct user

    directs.update(is_read= True)

    if(request.method == 'POST'):
        form= SendMessageForm(request.POST)
        if form.is_valid():
            body= form.cleaned_data['body']
            to_user= User.objects.get(username= active_direct)          
            Message.send_message(from_user=user, to_user= to_user, body=body)
            form= SendMessageForm()
        else:
            form= SendMessageForm()

    else:
        form= SendMessageForm()

    for message in messages:
        if message['user'].username== active_direct:
            message['unread']= 0
    
    context={
       'directs': directs, 
       'active_direct': active_direct, 
       'messages': messages ,
       'form': form
    }
    return render(request, 'chatapp/directs.html', context)

@login_required
def userSearch(request):
    query= request.GET.get('q','')
    if query:
        search_users= User.objects.filter(Q(profile__first_name__icontains= query) | Q(profile__last_name__icontains= query))
    else:
        search_users = User.objects.none()
    
    paginator = Paginator(search_users, 10)     # Create a Paginator object with 10 searched users per page
    page_number = request.GET.get('page')       # Get the page number from the GET parameters
    page_obj = paginator.get_page(page_number)  # Retrieve the corresponding page of items

    return render(request, 'chatapp/searchuser.html', {'search_users': page_obj})