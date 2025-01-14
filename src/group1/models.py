# models.py
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone_number = models.CharField(max_length=15, unique=True)
    mother_language = models.CharField(max_length=50)
    target_language = models.CharField(max_length=50)
    language_level = models.CharField(
        max_length=2,
        choices=[
            ("A1", "Beginner"),
            ("A2", "Elementary"),
            ("B1", "Intermediate"),
            ("B2", "Upper Intermediate"),
            ("C1", "Advanced"),
            ("C2", "Proficient")
        ],
    )
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    status = models.CharField(
        max_length=10,
        choices=[("online", "Online"), ("offline", "Offline")],
        default="offline"
    )

    def __str__(self):
        return self.user.username

class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="admin_groups")
    members = models.ManyToManyField(User, through="GroupMembership")
    created_at = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(upload_to="groups/avatars/", blank=True, null=True)

    def __str__(self):
        return self.name

class GroupRole(models.TextChoices):
    MEMBER = "member", "Member"
    ADMIN = "admin", "Admin"

class GroupMembership(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="membership")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="group_membership")
    role = models.CharField(max_length=10, choices=GroupRole.choices, default=GroupRole.MEMBER)

    class Meta:
        unique_together = ('group', 'user')

    def __str__(self):
        return f"{self.user.username} in group {self.group.name} as {self.role}"

class PrivateChat(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="private_chats_user1")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="private_chats_user2")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat between {self.user1.username} and {self.user2.username}"

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True, related_name="messages")
    private_chat = models.ForeignKey(PrivateChat, on_delete=models.CASCADE, blank=True, null=True, related_name="messages")
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="messages/images/", blank=True, null=True)
    video = models.FileField(upload_to="messages/videos/", blank=True, null=True)
    voice_note = models.FileField(upload_to="messages/voices/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.group:
            return f"Message in group {self.group.name}"
        return f"Message in private chat"

class Block(models.Model):
    blocker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blocks_initiated")
    blocked = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blocks_received")
    blocked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.blocker.username} blocked {self.blocked.username}"

class Report(models.Model):
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reports_made")
    reported_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reports_received")
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report by {self.reporter.username} against {self.reported_user.username}"

class LanguagePartner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="language_partner")
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

class FriendRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_requests")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_requests")
    status = models.CharField(
        max_length=10,
        choices=[("pending", "Pending"), ("accepted", "Accepted"), ("rejected", "Rejected")],
        default="pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Friend request from {self.sender.username} to {self.receiver.username}"
