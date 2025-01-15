# serializers.py
from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'mother_language', 'target_language', 'language_level', 'avatar', 'status']

class PrivateChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateChat
        fields = ['user1', 'user2', 'created_at']    
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['sender', 'private_chat', 'text', 'created_at']       
class GroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name', 'description']

    def create(self, validated_data):
        group = Group.objects.create(
            name=validated_data['name'],
            description=validated_data.get('description', ''),
            admin=self.context['request'].user
        )
        group.members.add(self.context['request'].user)
        return group             
class GroupMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['text']

    def create(self, validated_data):
        # گرفتن گروه از context یا فیلد گروه که در URL ارسال شده است
        group = self.context['group']
        message = Message.objects.create(
            sender=self.context['request'].user,
            group=group,
            text=validated_data['text']
        )
        return message
class AddGroupMemberSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

    def validate_user_id(self, value):
        try:
            user = User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")
        return value
class RemoveGroupMemberSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

    def validate_user_id(self, value):
        try:
            user = User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")
        return value

class LanguagePartnerSearchSerializer(serializers.Serializer):
    language = serializers.CharField(max_length=50)
    level = serializers.CharField(max_length=2)

    def validate(self, data):
        language = data.get('language')
        level = data.get('level')

        valid_levels = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
        if level not in valid_levels:
            raise serializers.ValidationError("Invalid language level.")
        return data            
class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ['username', 'password', 'profile']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user, **profile_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        return user