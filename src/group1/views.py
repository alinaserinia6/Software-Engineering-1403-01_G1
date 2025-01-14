# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import *
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.urls import reverse

# Home Page

# Home Page
def home(request):
    return render(request, 'group1.html', {'group_number': '1'})

# User Management APIs
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')
        mother_language = request.POST.get('mother_language')
        target_language = request.POST.get('target_language')
        language_level = request.POST.get('language_level')

        user = User.objects.create_user(username=username, password=password)
        UserProfile.objects.create(
            user=user,
            phone_number=phone_number,
            mother_language=mother_language,
            target_language=target_language,
            language_level=language_level,
        )
        return JsonResponse({'message': 'User registered successfully'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({'message': 'User logged in successfully'})
        return JsonResponse({'error': 'Invalid credentials'}, status=401)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def logout_user(request):
    logout(request)
    return JsonResponse({'message': 'User logged out successfully'})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.mother_language = request.POST.get('mother_language', user_profile.mother_language)
        user_profile.target_language = request.POST.get('target_language', user_profile.target_language)
        user_profile.language_level = request.POST.get('language_level', user_profile.language_level)
        user_profile.save()
        return JsonResponse({'message': 'Profile updated successfully'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

# Private Chat APIs
@login_required
def create_private_chat(request):
    user2_id = request.POST.get('user2_id')
    user2 = User.objects.get(id=user2_id)
    chat = PrivateChat.objects.create(user1=request.user, user2=user2)
    return JsonResponse({'message': 'Private chat created', 'chat_id': chat.id})

@login_required
def send_private_message(request):
    chat_id = request.POST.get('chat_id')
    text = request.POST.get('text')
    chat = PrivateChat.objects.get(id=chat_id)
    message = Message.objects.create(sender=request.user, private_chat=chat, text=text)
    return JsonResponse({'message': 'Message sent', 'message_id': message.id})

@login_required
def get_single_chat(request, chat_id):
    chat = PrivateChat.objects.filter(id=chat_id, user1=request.user) | PrivateChat.objects.filter(id=chat_id, user2=request.user)
    if not chat.exists():
        raise PermissionDenied("You are not part of this chat.")
    messages = Message.objects.filter(private_chat=chat.first()).values('id', 'sender__username', 'text', 'created_at')
    return JsonResponse({'messages': list(messages)})

# Group Chat APIs
@login_required
def create_group(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        group = Group.objects.create(name=name, description=description, admin=request.user)
        GroupMembership.objects.create(group=group, user=request.user, role=GroupRole.ADMIN)
        return JsonResponse({'message': 'Group created', 'group_id': group.id})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def send_group_message(request, group_id):
    group = Group.objects.get(id=group_id)
    membership = GroupMembership.objects.filter(group=group, user=request.user).first()
    if not membership:
        raise PermissionDenied("You are not a member of this group.")
    text = request.POST.get('text')
    message = Message.objects.create(sender=request.user, group=group, text=text)
    return JsonResponse({'message': 'Message sent', 'message_id': message.id})

@login_required
def add_group_member(request, group_id):
    group = Group.objects.get(id=group_id)
    membership = GroupMembership.objects.filter(group=group, user=request.user).first()
    if not membership or membership.role != GroupRole.ADMIN:
        raise PermissionDenied("You do not have permission to add members.")
    user_id = request.POST.get('user_id')
    user = User.objects.get(id=user_id)
    GroupMembership.objects.create(group=group, user=user)
    return JsonResponse({'message': 'Member added successfully'})

@login_required
def remove_group_member(request, group_id):
    group = Group.objects.get(id=group_id)
    membership = GroupMembership.objects.filter(group=group, user=request.user).first()
    if not membership or membership.role != GroupRole.ADMIN:
        raise PermissionDenied("You do not have permission to remove members.")
    user_id = request.POST.get('user_id')
    user = User.objects.get(id=user_id)
    GroupMembership.objects.filter(group=group, user=user).delete()
    return JsonResponse({'message': 'Member removed successfully'})

# Language Partner Matching
@login_required
def search_language_partners(request):
    language = request.GET.get('language')
    level = request.GET.get('level')
    partners = LanguagePartner.objects.filter(
        user__profile__target_language=language,
        user__profile__language_level=level,
        is_available=True,
    )
    data = [{'username': partner.user.username, 'id': partner.user.id} for partner in partners]
    return JsonResponse({'partners': data})

@login_required
def send_partner_request(request):
    receiver_id = request.POST.get('receiver_id')
    receiver = User.objects.get(id=receiver_id)
    FriendRequest.objects.create(sender=request.user, receiver=receiver)
    return JsonResponse({'message': 'Request sent'})

@login_required
def accept_partner_request(request):
    request_id = request.POST.get('request_id')
    friend_request = FriendRequest.objects.get(id=request_id, receiver=request.user)
    friend_request.status = 'accepted'
    friend_request.save()
    return JsonResponse({'message': 'Friend request accepted'})

# Reporting and Blocking
@login_required
def report_user(request):
    reported_user_id = request.POST.get('reported_user_id')
    reason = request.POST.get('reason')
    reported_user = User.objects.get(id=reported_user_id)
    Report.objects.create(reporter=request.user, reported_user=reported_user, reason=reason)
    return JsonResponse({'message': 'User reported'})

@login_required
def block_user(request):
    blocked_user_id = request.POST.get('blocked_user_id')
    blocked_user = User.objects.get(id=blocked_user_id)
    Block.objects.create(blocker=request.user, blocked=blocked_user)
    return JsonResponse({'message': 'User blocked'})

# User Retrieval APIs
@login_required
def get_all_users(request):
    users = User.objects.all().values('id', 'username', 'profile__avatar', 'profile__phone_number')
    return JsonResponse({'users': list(users)})

@login_required
def get_single_user(request, user_id):
    user = User.objects.filter(id=user_id).values('id', 'username', 'profile__avatar', 'profile__phone_number', 'profile__mother_language', 'profile__target_language').first()
    if not user:
        return JsonResponse({'error': 'User not found'}, status=404)
    return JsonResponse({'user': user})

# Chat Retrieval APIs
@login_required
def get_all_chats(request):
    chats = PrivateChat.objects.filter(user1=request.user) | PrivateChat.objects.filter(user2=request.user)
    data = [{'id': chat.id, 'user1': chat.user1.username, 'user2': chat.user2.username} for chat in chats]
    return JsonResponse({'chats': data})

# Additional APIs
@login_required
def get_user_avatar(request, user_id):
    user_profile = UserProfile.objects.filter(user_id=user_id).first()
    if not user_profile:
        return JsonResponse({'error': 'User not found'}, status=404)
    return JsonResponse({'avatar': user_profile.avatar.url if user_profile.avatar else None})

@login_required
def get_user_details(request, user_id):
    user_profile = UserProfile.objects.filter(user_id=user_id).first()
    if not user_profile:
        return JsonResponse({'error': 'User not found'}, status=404)
    return JsonResponse({
        'username': user_profile.user.username,
        'avatar': user_profile.avatar.url if user_profile.avatar else None,
        'phone_number': user_profile.phone_number
    })

# Message APIs
@login_required
def delete_message(request, message_id):
    try:
        message = Message.objects.get(id=message_id)
        if message.sender != request.user:
            raise PermissionDenied("You are not authorized to delete this message.")
        message.delete()
        return JsonResponse({'message': 'Message deleted successfully'})
    except Message.DoesNotExist:
        return JsonResponse({'error': 'Message not found'}, status=404)

@login_required
def edit_message(request, message_id):
    try:
        message = Message.objects.get(id=message_id)
        if message.sender != request.user:
            raise PermissionDenied("You are not authorized to edit this message.")
        if request.method == 'POST':
            new_text = request.POST.get('text', '')
            if not new_text:
                return JsonResponse({'error': 'Message text cannot be empty'}, status=400)
            message.text = new_text
            message.save()
            return JsonResponse({'message': 'Message edited successfully'})
    except Message.DoesNotExist:
        return JsonResponse({'error': 'Message not found'}, status=404)
