# views.py
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import *
from django.core.exceptions import PermissionDenied
from .serializers import UserProfileSerializer, PrivateChatSerializer, MessageSerializer, GroupCreateSerializer, GroupMessageSerializer, AddGroupMemberSerializer, RemoveGroupMemberSerializer, LanguagePartnerSearchSerializer, UserSerializer, LoginSerializer


from django.contrib.auth import login
from drf_yasg.utils import swagger_auto_schema


# Home Page
def home(request):
    return render(request, 'group1.html', {'group_number': '1'})

# User Management APIs
@swagger_auto_schema(method='post', request_body=UserSerializer)
@api_view(['POST'])
def register(request):
    """
    User registration API.
    URL: /register/
    Method: POST
    Payload: {
        "username": "string",
        "password": "string",
        "profile": {
            "phone_number": "string",
            "mother_language": "string",
            "target_language": "string",
            "language_level": "string",
            "avatar": "file",
            "status": "string"
        }
    }
    Response: {
        "message": "User registered successfully",
        "status": 201
    }
    """
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response({'error': 'Invalid request', 'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# Login API
@swagger_auto_schema(method='post', request_body=LoginSerializer)
@api_view(['POST'])
def login_user(request):
    """
    User login API.
    URL: /login/
    Method: POST
    Payload: {
        "username": "string",
        "password": "string"
    }
    Response: {
        "message": "User logged in successfully",
        "status": 200
    }
    """
    if request.method == 'POST':
        try:
            # Serialize the input data
            serializer = LoginSerializer(data=request.data)
            
            # Validate the serializer
            if serializer.is_valid():
                user = serializer.validated_data  # This will be the user object returned by validate()

                # If the user is found, login the user
                login(request, user)
                
                return Response({'message': 'User logged in successfully'}, status=status.HTTP_200_OK)
            
            # If the serializer is invalid, return errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# Logout API
@swagger_auto_schema(method='post')
@api_view(['POST'])
def logout_user(request):
    """
    User logout API.
    URL: /logout/
    Method: POST
    Response: {
        "message": "User logged out successfully",
        "status": 200
    }
    """
    logout(request)
    return Response({'message': 'User logged out successfully'}, status=status.HTTP_200_OK)

# Edit Profile API
@swagger_auto_schema(method='post', request_body=UserProfileSerializer)
@api_view(['POST'])
def edit_profile(request):
    """
    Edit user profile API.
    URL: /edit_profile/
    Method: POST
    Payload: {
        "mother_language": "string",
        "target_language": "string",
        "language_level": "string"
    }
    Response: {
        "message": "Profile updated successfully",
        "status": 200
    }
    """
    if request.method == 'POST':
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.mother_language = request.data.get('mother_language', user_profile.mother_language)
        user_profile.target_language = request.data.get('target_language', user_profile.target_language)
        user_profile.language_level = request.data.get('language_level', user_profile.language_level)
        user_profile.save()
        return Response({'message': 'Profile updated successfully'}, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
# Private Chat APIs

# Private Chat APIs

# Private Chat API - Create Private Chat
@swagger_auto_schema(method='post', request_body=PrivateChatSerializer)
@api_view(['POST'])
def create_private_chat(request):
    """
    Create a private chat API.
    URL: /create_private_chat/
    Method: POST
    Payload: {
        "user2_id": "integer"
    }
    Response: {
        "message": "Private chat created",
        "chat_id": "integer",
        "status": 201
    }
    """
    if request.method == 'POST':
        user2_id = request.data.get('user2_id')
        try:
            user2 = User.objects.get(id=user2_id)
            chat = PrivateChat.objects.create(user1=request.user, user2=user2)
            return Response({'message': 'Private chat created', 'chat_id': chat.id}, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='post', request_body=MessageSerializer)
@api_view(['POST'])
def send_private_message(request):
    """
    Send a private message API.
    URL: /send_private_message/
    Method: POST
    Payload: {
        "chat_id": "integer",
        "text": "string"
    }
    Response: {
        "message": "Message sent",
        "message_id": "integer",
        "status": 201
    }
    """
    if request.method == 'POST':
        chat_id = request.data.get('chat_id')
        text = request.data.get('text')

        try:
            chat = PrivateChat.objects.get(id=chat_id)
            message = Message.objects.create(sender=request.user, private_chat=chat, text=text)
            return Response({'message': 'Message sent', 'message_id': message.id}, status=status.HTTP_201_CREATED)
        except PrivateChat.DoesNotExist:
            return Response({'error': 'Chat not found'}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='get', responses={200: 'OK'})
@api_view(['GET'])
def get_single_chat(request, chat_id):
    """
    Get messages from a single private chat.
    URL: /private-chat/{chat_id}/
    Method: GET
    Params: chat_id (path param)
    Response: {
        "messages": [
            {
                "id": "int",
                "sender__username": "string",
                "text": "string",
                "created_at": "datetime"
            }
        ]
    }
    """
    chat = PrivateChat.objects.filter(id=chat_id, user1=request.user) | PrivateChat.objects.filter(id=chat_id, user2=request.user)
    
    if not chat.exists():
        raise PermissionDenied("You are not part of this chat.")
    
    messages = Message.objects.filter(private_chat=chat.first()).values('id', 'sender__username', 'text', 'created_at')
    return Response({'messages': list(messages)}, status=status.HTTP_200_OK)

@swagger_auto_schema(method='post', request_body=GroupCreateSerializer)
@api_view(['POST'])
def create_group(request):
    """
    Create a new group.
    URL: /create-group/
    Method: POST
    Payload: {
        "name": "string",
        "description": "string"
    }
    Response: {
        "message": "Group created",
        "group_id": "int"
    }
    """
    name = request.data.get('name')
    description = request.data.get('description')

    if not name or not description:
        return Response({'error': 'Name and description are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    group = Group.objects.create(name=name, description=description, admin=request.user)
    GroupMembership.objects.create(group=group, user=request.user, role=GroupRole.ADMIN)
    return Response({'message': 'Group created', 'group_id': group.id}, status=status.HTTP_201_CREATED)

@swagger_auto_schema(method='post', request_body=GroupMessageSerializer)
@api_view(['POST'])
def send_group_message(request, group_id):
    """
    Send a message to a group.
    URL: /send-group-message/{group_id}/
    Method: POST
    Payload: {
        "text": "string"
    }
    Response: {
        "message": "Message sent",
        "message_id": "int"
    }
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

@swagger_auto_schema(method='post', request_body=AddGroupMemberSerializer)
@api_view(['POST'])
def add_group_member(request, group_id):
    """
    Add a new member to a group.
    URL: /groups/{group_id}/add_member/
    Method: POST
    Payload: {
        "user_id": "integer"
    }
    Response: {
        "message": "Member added successfully",
        "status": 201
    }
    """
    try:
        group = Group.objects.get(id=group_id)
        membership = GroupMembership.objects.filter(group=group, user=request.user).first()
        if not membership or membership.role != 'admin':
            raise PermissionDenied("You do not have permission to add members.")
        
        serializer = AddGroupMemberSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            user = User.objects.get(id=user_id)
            GroupMembership.objects.create(group=group, user=user)
            return Response({'message': 'Member added successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Group.DoesNotExist:
        return Response({'error': 'Group not found'}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='post', request_body=RemoveGroupMemberSerializer)
@api_view(['POST'])
def remove_group_member(request, group_id):
    """
    Remove a member from a group.
    URL: /groups/{group_id}/remove_member/
    Method: POST
    Payload: {
        "user_id": "integer"
    }
    Response: {
        "message": "Member removed successfully",
        "status": 200
    }
    """
    try:
        group = Group.objects.get(id=group_id)
        membership = GroupMembership.objects.filter(group=group, user=request.user).first()
        if not membership or membership.role != 'admin':
            raise PermissionDenied("You do not have permission to remove members.")
        
        serializer = RemoveGroupMemberSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            user = User.objects.get(id=user_id)
            GroupMembership.objects.filter(group=group, user=user).delete()
            return Response({'message': 'Member removed successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Group.DoesNotExist:
        return Response({'error': 'Group not found'}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)

# Language Partner Matching API
@swagger_auto_schema(method='get', request_body=LanguagePartnerSearchSerializer)
@api_view(['GET'])
def search_language_partners(request):
    """
    Search for available language partners based on target language and level.
    URL: /language_partners/search/
    Method: GET
    Query Parameters: 
        language: "string"
        level: "string"
    Response: {
        "partners": [{"username": "string", "id": "integer"}],
        "status": 200
    }
    """
    serializer = LanguagePartnerSearchSerializer(data=request.query_params)
    if serializer.is_valid():
        language = serializer.validated_data['language']
        level = serializer.validated_data['level']

        partners = LanguagePartner.objects.filter(
            user__profile__target_language=language,
            user__profile__language_level=level,
            is_available=True,
        )

        if partners.exists():
            data = [{'username': partner.user.username, 'id': partner.user.id} for partner in partners]
            return Response({'partners': data}, status=status.HTTP_200_OK)
        return Response({'error': 'No partners found'}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@swagger_auto_schema(method='post')
@api_view(['POST'])
def send_partner_request(request):
    """
    Send a friend request to another user.
    URL: /send_partner_request/
    Method: POST
    Payload: {
        "receiver_id": "integer"
    }
    Response: {
        "message": "Request sent",
        "status": 201
    }
    """
    try:
        receiver_id = request.data.get('receiver_id')
        receiver = User.objects.get(id=receiver_id)
        FriendRequest.objects.create(sender=request.user, receiver=receiver)
        return Response({'message': 'Request sent'}, status=status.HTTP_201_CREATED)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='post')
@api_view(['POST'])
def accept_partner_request(request):
    """
    Accept a pending friend request.
    URL: /accept_partner_request/
    Method: POST
    Payload: {
        "request_id": "integer"
    }
    Response: {
        "message": "Friend request accepted",
        "status": 200
    }
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

@swagger_auto_schema(method='post')
@api_view(['POST'])
def report_user(request):
    """
    Report a user for inappropriate behavior.
    URL: /report_user/
    Method: POST
    Payload: {
        "reported_user_id": "integer",
        "reason": "string"
    }
    Response: {
        "message": "User reported",
        "status": 201
    }
    """
    try:
        reported_user_id = request.data.get('reported_user_id')
        reason = request.data.get('reason')
        reported_user = User.objects.get(id=reported_user_id)
        Report.objects.create(reporter=request.user, reported_user=reported_user, reason=reason)
        return Response({'message': 'User reported'}, status=status.HTTP_201_CREATED)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)
@swagger_auto_schema(method='post')
@api_view(['POST'])
def block_user(request):
    """
    Block a user from interacting with the current user.
    URL: /block_user/
    Method: POST
    Payload: {
        "blocked_user_id": "integer"
    }
    Response: {
        "message": "User blocked",
        "status": 201
    }
    """
    try:
        blocked_user_id = request.data.get('blocked_user_id')
        blocked_user = User.objects.get(id=blocked_user_id)
        Block.objects.create(blocker=request.user, blocked=blocked_user)
        return Response({'message': 'User blocked'}, status=status.HTTP_201_CREATED)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)
# User Retrieval APIs
@swagger_auto_schema(method='get')
@api_view(['GET'])
def get_all_users(request):
    """
    Get a list of all users with basic profile information.
    URL: /get_all_users/
    Method: GET
    Response: {
        "users": [
            {
                "id": "integer",
                "username": "string",
                "profile__avatar": "string",
                "profile__phone_number": "string"
            }
        ]
    }
    """
    users = User.objects.all().values('id', 'username', 'profile__avatar', 'profile__phone_number')
    return Response({'users': list(users)}, status=status.HTTP_200_OK)
@swagger_auto_schema(method='get')
@api_view(['GET'])
def get_single_user(request, user_id):
    """
    Get details of a single user by their user ID.
    URL: /get_single_user/{user_id}/
    Method: GET
    Response: {
        "user": {
            "id": "integer",
            "username": "string",
            "profile_avatar": "string",
            "profile_phone_number": "string",
            "profile_mother_language": "string",
            "profile_target_language": "string"
        }
    }
    """
    user = User.objects.filter(id=user_id).values('id', 'username', 'profile__avatar', 'profile__phone_number', 'profile__mother_language', 'profile__target_language').first()
    if not user:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'user': user}, status=status.HTTP_200_OK)

@swagger_auto_schema(method='get', responses={200: PrivateChatSerializer(many=True)})
@api_view(['GET'])
def get_all_chats(request):
    """
    Get a list of all chats for the current user.
    URL: /get_all_chats/
    Method: GET
    Response: {
        "chats": [
            {
                "id": "integer",
                "user1": "string",
                "user2": "string"
            }
        ]
    }
    """
    chats = PrivateChat.objects.filter(user1=request.user) | PrivateChat.objects.filter(user2=request.user)
    data = [{'id': chat.id, 'user1': chat.user1.username, 'user2': chat.user2.username} for chat in chats]
    return Response({'chats': data}, status=status.HTTP_200_OK)

@swagger_auto_schema(method='get')
@api_view(['GET'])
def get_user_avatar(request, user_id):
    """
    Get the avatar of a user by their user ID.
    URL: /get_user_avatar/{user_id}/
    Method: GET
    Response: {
        "avatar": "string"
    }
    """
    user_profile = UserProfile.objects.filter(user_id=user_id).first()
    if not user_profile:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'avatar': user_profile.avatar.url if user_profile.avatar else None}, status=status.HTTP_200_OK)
@swagger_auto_schema(method='get')
@api_view(['GET'])
def get_user_details(request, user_id):
    """
    Get the details of a user by their user ID.
    URL: /get_user_details/{user_id}/
    Method: GET
    Response: {
        "username": "string",
        "avatar": "string",
        "phone_number": "string"
    }
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
@swagger_auto_schema(method='delete', responses={200})
@api_view(['DELETE'])
def delete_message(request, message_id):
    """
    Delete a message if the user is the sender.
    URL: /delete_message/{message_id}/
    Method: DELETE
    Response: {
        "message": "Message deleted successfully"
    }
    """
    try:
        message = Message.objects.get(id=message_id)
        if message.sender != request.user:
            raise PermissionDenied("You are not authorized to delete this message.")
        message.delete()
        return Response({'message': 'Message deleted successfully'}, status=status.HTTP_200_OK)
    except Message.DoesNotExist:
        return Response({'error': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)

@swagger_auto_schema(method='post')
@api_view(['POST'])
def edit_message(request, message_id):
    """
    Edit a message if the user is the sender.
    URL: /edit_message/{message_id}/
    Method: POST
    Payload: {
        "text": "string"
    }
    Response: {
        "message": "Message edited successfully"
    }
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
