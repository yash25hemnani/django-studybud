from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message
from .forms import RoomForm, MessageForm, UserForm

rooms = [
    {"id":1, "name": "Room 1"},
    {"id":2, "name": "Room 2"},
    {"id":3, "name": "Room 3"},
]

# Create your views here.


def home(request):
    return redirect('room_function')

def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('room_function')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, 'User Does Not Exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('room_function')
        else:
            messages.error(request, 'Incorrect Username or Password')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('room_function')

def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) #Helps you get the user value immediately
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('room_function')
        else:
            messages.error(request, 'An error occured during registration.')


    return render(request, 'base/login_register.html', {'form':form})


def room_function(request):
    q = request.GET.get('q') if (request.GET.get('q') != None) else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | 
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()
    room_count = rooms.count()

    room_messages =  Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {"rooms":rooms, "topics":topics, "room_count": room_count, "room_messages":room_messages}
    return render(request, 'base/room.html', context)

def solo_room(request, id):
    get_room = Room.objects.get(id = id)
    room_messages = get_room.message_set.all() # Don't name it messages, else it will refer to the flash messages as well
    participants = get_room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = get_room,
            body = request.POST.get('body')
        )
        get_room.participants.add(request.user)
        
        return redirect('solo_room', id = get_room.id)

    context = {"room":get_room, "room_messages":room_messages, "participants":participants}
    return render(request, 'base/solo_room.html', context)

def userProfile(request, id):
    user = User.objects.get(id=id)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user':user, 'rooms':rooms, 'room_messages': room_messages, 'topics':topics}
    return render(request, 'base/profile.html', context)

@login_required(login_url=loginPage)
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created =Topic.objects.get_or_create(name=topic_name) #This will create a new field if topic doesnt exist (cretaed will be true here) or if it does, it'll get the obejct (cretaed will be false here)

        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description')
        )
        return redirect('room_function')
        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.save()

    context = {'form': form, 'topics':topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url="loginPage")
def updateRoom(request, id):
    room = Room.objects.get(id= id)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('Wrong User!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        # form = RoomForm(request.POST, instance=room)
        # if form.is_valid:
        #     form.save()
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('room_function')

    context = {'form':form, 'topics':topics, 'room': room}
    return render(request, 'base/room_form.html', context)

@login_required(login_url=loginPage)
def deleteRoom(request, id):
    room = Room.objects.get(id=id)

    if request.user != room.host:
        return HttpResponse('Wrong User!!')
    
    if request.method == 'POST':
        room.delete()
        return redirect('room_function')
    return render(request, 'base/delete.html', {'obj': room})

@login_required(login_url=loginPage)
def deleteMessage(request, id):
    message = Message.objects.get(id=id)

    if request.user != message.user:
        return HttpResponse('Wrong User!!')
    
    if request.method == 'POST':
        message.delete()
        return redirect('room_function')
    return render(request, 'base/delete.html', {'obj': message})

@login_required(login_url="loginPage")
def editMessage(request, roomid, id):
    message = Message.objects.get(id=id)
    form = MessageForm(instance=message)

    if request.user != message.user:
        return HttpResponse('Invalid User')
    
    if request.method == 'POST':
        form = MessageForm(request.POST, instance=message)
        if form.is_valid:
            form.save()
            return redirect(f'/room/{roomid}')
        
    context = {'form':form}
    return render(request, 'base/message_form.html', context)

@login_required(login_url="loginPage")
def updateUser(request):
    user = request.user
    form = UserForm(instance=request.user)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_profile', id=user.id)

    return render(request, 'base/update_user.html', {'form':form})