from django.db import models
from django.contrib.auth.models import User

class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_groups', related_query_name='admin_group') #are this needed?
    members = models.ManyToManyField(User, related_name='group_memberships', related_query_name='group_member')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class PrivateChat(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='private_chats_user1', related_query_name='private_chat_user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='private_chats_user2', related_query_name='private_chat_user2')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat between {self.user1.username} and {self.user2.username}"

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages', related_query_name='sent_message')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True, related_name='messages', related_query_name='message')
    private_chat = models.ForeignKey(PrivateChat, on_delete=models.CASCADE, blank=True, null=True, related_name='messages', related_query_name='message')
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='group1/images/', blank=True, null=True)
    video = models.FileField(upload_to='group1/videos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.group:
            return f"Message from {self.sender.username} in group {self.group.name}"
        elif self.private_chat:
            return f"Message from {self.sender.username} in private chat"
        return f"Message from {self.sender.username}"

class Block(models.Model):
    blocker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocker', related_query_name='blocker_user')
    blocked = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked', related_query_name='blocked_user')
    blocked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.blocker.username} blocked {self.blocked.username}"
