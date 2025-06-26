from django.db import models
from app_modules.adminapp.models import User

# Create your models here.


class DirectChat(models.Model):
    user1 = models.ForeignKey(User, related_name="user1_chats", on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name="user2_chats", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1','user2')
        
    def __str__(self):
        return f"Chat between {self.user1.username} and {self.user2.username}"

class Message(models.Model):
    room = models.ForeignKey(DirectChat, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    media_file = models.FileField(upload_to='chat/media/', blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content if self.content else 'Media'}"