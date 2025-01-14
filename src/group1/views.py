# views.py
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import *
from django.core.exceptions import PermissionDenied


# Home Page
def home(request):
    return render(request, 'group1.html', {'group_number': '1'})

# User Management APIs
@api_view(['POST'])
def register(request):
    """
    User registration API.
    ---
    parameters:
      - name: username
        type: string
        required: true
      - name: password
        type: string
        required: true
      - name: phone_number
        type: string
        required: true
      - name: mother_language
        type: string
        required: true
      - name: target_language
        type: string
        required: true
      - name: language_level
        type: string
        required: true
    responses:
      200:
        description: User registered successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "User registered successfully"
      400:
        description: Invalid request
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Invalid request"
    """
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        phone_number = request.data.get('phone_number')
        mother_language = request.data.get('mother_language')
        target_language = request.data.get('target_language')
        language_level = request.data.get('language_level')

        user = User.objects.create_user(username=username, password=password)
        UserProfile.objects.create(
            user=user,
            phone_number=phone_number,
            mother_language=mother_language,
            target_language=target_language,
            language_level=language_level,
        )
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
    return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)


# Login API
@api_view(['POST'])
def login_user(request):
    """
    User login API.
    ---
    parameters:
      - name: username
        type: string
        required: true
      - name: password
        type: string
        required: true
    responses:
      200:
        description: User logged in successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "User logged in successfully"
      401:
        description: Invalid credentials
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Invalid credentials"
      400:
        description: Invalid request
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Invalid request"
    """
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return Response({'message': 'User logged in successfully'})
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)


# Logout API
@api_view(['POST'])
def logout_user(request):
    """
    User logout API.
    ---
    responses:
      200:
        description: User logged out successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "User logged out successfully"
    """
    logout(request)
    return Response({'message': 'User logged out successfully'}, status=status.HTTP_200_OK)


# Edit Profile API
@api_view(['POST'])
def edit_profile(request):
    """
    Edit user profile API.
    ---
    parameters:
      - name: mother_language
        type: string
        required: false
      - name: target_language
        type: string
        required: false
      - name: language_level
        type: string
        required: false
    responses:
      200:
        description: Profile updated successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Profile updated successfully"
      400:
        description: Invalid request
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Invalid request"
    """
    if request.method == 'POST':
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.mother_language = request.data.get('mother_language', user_profile.mother_language)
        user_profile.target_language = request.data.get('target_language', user_profile.target_language)
        user_profile.language_level = request.data.get('language_level', user_profile.language_level)
        user_profile.save()
        return Response({'message': 'Profile updated successfully'})
    return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

# Private Chat APIs

# Private Chat APIs

@api_view(['POST'])
def create_private_chat(request):
    """
    Create a private chat between two users.
    ---
    parameters:
      - name: user2_id
        type: integer
        required: true
    responses:
      200:
        description: Private chat created successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Private chat created"
            chat_id:
              type: integer
              example: 1
      400:
        description: Invalid request
        schema:
          type: object
          properties:
            error:
              type: string
              example: "User not found"
    """
    user2_id = request.data.get('user2_id')
    try:
        user2 = User.objects.get(id=user2_id)
        chat = PrivateChat.objects.create(user1=request.user, user2=user2)
        return Response({'message': 'Private chat created', 'chat_id': chat.id}, status=status.HTTP_201_CREATED)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def send_private_message(request):
    """
    Send a private message in an existing chat.
    ---
    parameters:
      - name: chat_id
        type: integer
        required: true
      - name: text
        type: string
        required: true
    responses:
      200:
        description: Message sent successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Message sent"
            message_id:
              type: integer
              example: 1
      400:
        description: Invalid request
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Chat not found"
    """
    chat_id = request.data.get('chat_id')
    text = request.data.get('text')

    try:
        chat = PrivateChat.objects.get(id=chat_id)
        message = Message.objects.create(sender=request.user, private_chat=chat, text=text)
        return Response({'message': 'Message sent', 'message_id': message.id}, status=status.HTTP_201_CREATED)
    except PrivateChat.DoesNotExist:
        return Response({'error': 'Chat not found'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_single_chat(request, chat_id):
    """
    Get all messages from a single private chat.
    ---
    parameters:
      - name: chat_id
        type: integer
        required: true
    responses:
      200:
        description: Messages retrieved successfully
        schema:
          type: object
          properties:
            messages:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  sender:
                    type: string
                    example: "user1"
                  text:
                    type: string
                    example: "Hello!"
                  created_at:
                    type: string
                    example: "2023-10-05T15:30:00Z"
      400:
        description: Invalid request
        schema:
          type: object
          properties:
            error:
              type: string
              example: "You are not part of this chat"
    """
    chat = PrivateChat.objects.filter(id=chat_id, user1=request.user) | PrivateChat.objects.filter(id=chat_id, user2=request.user)
    
    if not chat.exists():
        raise PermissionDenied("You are not part of this chat.")
    
    messages = Message.objects.filter(private_chat=chat.first()).values('id', 'sender__username', 'text', 'created_at')
    return Response({'messages': list(messages)}, status=status.HTTP_200_OK)


# Group Chat APIs

@api_view(['POST'])
def create_group(request):
    """
    Create a new group chat.
    ---
    parameters:
      - name: name
        type: string
        required: true
      - name: description
        type: string
        required: true
    responses:
      200:
        description: Group created successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Group created"
            group_id:
              type: integer
              example: 1
      400:
        description: Invalid request
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Invalid request"
    """
    name = request.data.get('name')
    description = request.data.get('description')

    if not name or not description:
        return Response({'error': 'Name and description are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    group = Group.objects.create(name=name, description=description, admin=request.user)
    GroupMembership.objects.create(group=group, user=request.user, role=GroupRole.ADMIN)
    return Response({'message': 'Group created', 'group_id': group.id}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def send_group_message(request, group_id):
    """
    Send a message in a group chat.
    ---
    parameters:
      - name: group_id
        type: integer
        required: true
      - name: text
        type: string
        required: true
    responses:
      200:
        description: Message sent successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Message sent"
            message_id:
              type: integer
              example: 1
      400:
        description: Invalid request
        schema:
          type: object
          properties:
            error:
              type: string
              example: "You are not a member of this group"
    """
    try:
        group = Group.objects.get(id=group_id)
        membership = GroupMembership.objects.filter(group=group, user=request.user).first()
        if not membership:
            raise PermissionDenied("You are not a member of this group.")
        
        text = request.data.get('text')
        message = Message.objects.create(sender=request.user, group=group, text=text)
        return Response({'message': 'Message sent', 'message_id': message.id}, status=status.HTTP_201_CREATED)
    except Group.DoesNotExist:
        return Response({'error': 'Group not found'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def add_group_member(request, group_id):
    """
    Add a member to a group chat.
    ---
    parameters:
      - name: group_id
        type: integer
        required: true
      - name: user_id
        type: integer
        required: true
    responses:
      200:
        description: Member added successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Member added successfully"
      400:
        description: Invalid request
        schema:
          type: object
          properties:
            error:
              type: string
              example: "You do not have permission to add members"
    """
    try:
        group = Group.objects.get(id=group_id)
        membership = GroupMembership.objects.filter(group=group, user=request.user).first()
        if not membership or membership.role != GroupRole.ADMIN:
            raise PermissionDenied("You do not have permission to add members.")
        
        user_id = request.data.get('user_id')
        user = User.objects.get(id=user_id)
        GroupMembership.objects.create(group=group, user=user)
        return Response({'message': 'Member added successfully'}, status=status.HTTP_201_CREATED)
    except Group.DoesNotExist:
        return Response({'error': 'Group not found'}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def remove_group_member(request, group_id):
    """
    Remove a member from a group chat.
    ---
    parameters:
      - name: group_id
        type: integer
        required: true
      - name: user_id
        type: integer
        required: true
    responses:
      200:
        description: Member removed successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Member removed successfully"
      400:
        description: Invalid request
        schema:
          type: object
          properties:
            error:
              type: string
              example: "You do not have permission to remove members"
    """
    try:
        group = Group.objects.get(id=group_id)
        membership = GroupMembership.objects.filter(group=group, user=request.user).first()
        if not membership or membership.role != GroupRole.ADMIN:
            raise PermissionDenied("You do not have permission to remove members.")
        
        user_id = request.data.get('user_id')
        user = User.objects.get(id=user_id)
        GroupMembership.objects.filter(group=group, user=user).delete()
        return Response({'message': 'Member removed successfully'}, status=status.HTTP_200_OK)
    except Group.DoesNotExist:
        return Response({'error': 'Group not found'}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)


# Language Partner Matching API

@api_view(['GET'])
def search_language_partners(request):
    """
    Search for language partners based on language and level.
    ---
    parameters:
      - name: language
        type: string
        required: true
      - name: level
        type: string
        required: true
    responses:
      200:
        description: Language partners found
        schema:
          type: object
          properties:
            partners:
              type: array
              items:
                type: object
                properties:
                  username:
                    type: string
                    example: "john_doe"
                  id:
                    type: integer
                    example: 1
      400:
        description: Invalid request
        schema:
          type: object
          properties:
            error:
              type: string
              example: "No partners found"
    """
    language = request.GET.get('language')
    level = request.GET.get('level')

    partners = LanguagePartner.objects.filter(
        user__profile__target_language=language,
        user__profile__language_level=level,
        is_available=True,
    )
    
    if partners.exists():
        data = [{'username': partner.user.username, 'id': partner.user.id} for partner in partners]
        return Response({'partners': data}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'No partners found'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def send_partner_request(request):
    """
    Send a friend request to another user.
    ---
    parameters:
      - name: receiver_id
        type: integer
        required: true
    responses:
      200:
        description: Request sent successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Request sent"
      400:
        description: Invalid request
        schema:
          type: object
          properties:
            error:
              type: string
              example: "User not found"
    """
    try:
        receiver_id = request.data.get('receiver_id')
        receiver = User.objects.get(id=receiver_id)
        FriendRequest.objects.create(sender=request.user, receiver=receiver)
        return Response({'message': 'Request sent'}, status=status.HTTP_201_CREATED)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def accept_partner_request(request):
    """
    Accept a pending friend request.
    ---
    parameters:
      - name: request_id
        type: integer
        required: true
    responses:
      200:
        description: Friend request accepted successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Friend request accepted"
      400:
        description: Invalid request
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Friend request not found or invalid"
    """
    try:
        request_id = request.data.get('request_id')
        friend_request = FriendRequest.objects.get(id=request_id, receiver=request.user)
        friend_request.status = 'accepted'
        friend_request.save()
        return Response({'message': 'Friend request accepted'}, status=status.HTTP_200_OK)
    except FriendRequest.DoesNotExist:
        return Response({'error': 'Friend request not found or invalid'}, status=status.HTTP_400_BAD_REQUEST)


# Reporting and Blocking APIs

@api_view(['POST'])
def report_user(request):
    """
    Report a user for inappropriate behavior.
    ---
    parameters:
      - name: reported_user_id
        type: integer
        required: true
      - name: reason
        type: string
        required: true
    responses:
      200:
        description: User reported successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "User reported"
      400:
        description: Invalid request
        schema:
          type: object
          properties:
            error:
              type: string
              example: "User not found"
    """
    try:
        reported_user_id = request.data.get('reported_user_id')
        reason = request.data.get('reason')
        reported_user = User.objects.get(id=reported_user_id)
        Report.objects.create(reporter=request.user, reported_user=reported_user, reason=reason)
        return Response({'message': 'User reported'}, status=status.HTTP_201_CREATED)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def block_user(request):
    """
    Block a user to prevent further interactions.
    ---
    parameters:
      - name: blocked_user_id
        type: integer
        required: true
    responses:
      200:
        description: User blocked successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "User blocked"
      400:
        description: Invalid request
        schema:
          type: object
          properties:
            error:
              type: string
              example: "User not found"
    """
    try:
        blocked_user_id = request.data.get('blocked_user_id')
        blocked_user = User.objects.get(id=blocked_user_id)
        Block.objects.create(blocker=request.user, blocked=blocked_user)
        return Response({'message': 'User blocked'}, status=status.HTTP_201_CREATED)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)

# User Retrieval APIs
@api_view(['GET'])
def get_all_users(request):
    """
    Get a list of all users with basic profile information.
    ---
    responses:
      200:
        description: List of all users
        schema:
          type: object
          properties:
            users:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  username:
                    type: string
                  profile:
                    type: object
                    properties:
                      avatar:
                        type: string
                      phone_number:
                        type: string
    """
    users = User.objects.all().values('id', 'username', 'profile__avatar', 'profile__phone_number')
    return Response({'users': list(users)}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_single_user(request, user_id):
    """
    Get detailed information of a single user.
    ---
    parameters:
      - name: user_id
        type: integer
        required: true
    responses:
      200:
        description: User found successfully
        schema:
          type: object
          properties:
            user:
              type: object
              properties:
                id:
                  type: integer
                username:
                  type: string
                profile:
                  type: object
                  properties:
                    avatar:
                      type: string
                    phone_number:
                      type: string
                    mother_language:
                      type: string
                    target_language:
                      type: string
      404:
        description: User not found
        schema:
          type: object
          properties:
            error:
              type: string
              example: "User not found"
    """
    user = User.objects.filter(id=user_id).values('id', 'username', 'profile__avatar', 'profile__phone_number', 'profile__mother_language', 'profile__target_language').first()
    if not user:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'user': user}, status=status.HTTP_200_OK)


# Chat Retrieval APIs

@api_view(['GET'])
def get_all_chats(request):
    """
    Get a list of all chats for the logged-in user.
    ---
    responses:
      200:
        description: List of all chats
        schema:
          type: object
          properties:
            chats:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  user1:
                    type: string
                  user2:
                    type: string
    """
    chats = PrivateChat.objects.filter(user1=request.user) | PrivateChat.objects.filter(user2=request.user)
    data = [{'id': chat.id, 'user1': chat.user1.username, 'user2': chat.user2.username} for chat in chats]
    return Response({'chats': data}, status=status.HTTP_200_OK)


# Additional API

@api_view(['GET'])
def get_user_avatar(request, user_id):
    """
    Get the avatar of a user.
    ---
    parameters:
      - name: user_id
        type: integer
        required: true
    responses:
      200:
        description: Avatar URL of the user
        schema:
          type: object
          properties:
            avatar:
              type: string
      404:
        description: User not found
        schema:
          type: object
          properties:
            error:
              type: string
              example: "User not found"
    """
    user_profile = UserProfile.objects.filter(user_id=user_id).first()
    if not user_profile:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'avatar': user_profile.avatar.url if user_profile.avatar else None}, status=status.HTTP_200_OK)
@api_view(['GET'])
def get_user_details(request, user_id):
    """
    Get user details including username, avatar, and phone number.
    ---
    parameters:
      - name: user_id
        type: integer
        required: true
    responses:
      200:
        description: User details found
        schema:
          type: object
          properties:
            username:
              type: string
            avatar:
              type: string
            phone_number:
              type: string
      404:
        description: User not found
        schema:
          type: object
          properties:
            error:
              type: string
              example: "User not found"
    """
    user_profile = UserProfile.objects.filter(user_id=user_id).first()
    if not user_profile:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    return Response({
        'username': user_profile.user.username,
        'avatar': user_profile.avatar.url if user_profile.avatar else None,
        'phone_number': user_profile.phone_number
    }, status=status.HTTP_200_OK)


# Message APIs

@api_view(['DELETE'])
def delete_message(request, message_id):
    """
    Delete a specific message if the requester is the sender.
    ---
    parameters:
      - name: message_id
        type: integer
        required: true
    responses:
      200:
        description: Message deleted successfully
      404:
        description: Message not found
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Message not found"
      403:
        description: Unauthorized to delete message
        schema:
          type: object
          properties:
            error:
              type: string
              example: "You are not authorized to delete this message."
    """
    try:
        message = Message.objects.get(id=message_id)
        if message.sender != request.user:
            raise PermissionDenied("You are not authorized to delete this message.")
        message.delete()
        return Response({'message': 'Message deleted successfully'}, status=status.HTTP_200_OK)
    except Message.DoesNotExist:
        return Response({'error': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def edit_message(request, message_id):
    """
    Edit a specific message if the requester is the sender.
    ---
    parameters:
      - name: message_id
        type: integer
        required: true
      - name: text
        type: string
        required: true
        description: New message text
    responses:
      200:
        description: Message edited successfully
      400:
        description: Message text cannot be empty
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Message text cannot be empty"
      404:
        description: Message not found
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Message not found"
      403:
        description: Unauthorized to edit message
        schema:
          type: object
          properties:
            error:
              type: string
              example: "You are not authorized to edit this message."
    """
    try:
        message = Message.objects.get(id=message_id)
        if message.sender != request.user:
            raise PermissionDenied("You are not authorized to edit this message.")
        new_text = request.data.get('text', '')
        if not new_text:
            return Response({'error': 'Message text cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)
        message.text = new_text
        message.save()
        return Response({'message': 'Message edited successfully'}, status=status.HTTP_200_OK)
    except Message.DoesNotExist:
        return Response({'error': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)