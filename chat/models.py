import uuid 

from django.db import models
from django.contrib.auth import get_user_model


CustomUser = get_user_model()


class Inbox(models.Model):
    
    secondary_id = models.UUIDField(default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(CustomUser, blank=True, related_name="inboxes")
    
    
    def name(self, request_participant_id):
        other_participant = self.participants.exclude(id=request_participant_id).first()
        return other_participant.username
        
    
    
class Message(models.Model):
    
    secondary_id = models.UUIDField(default=uuid.uuid4, editable=False)
    inbox = models.ForeignKey(Inbox, related_name="messages", on_delete=models.CASCADE)
    sender = models.ForeignKey(CustomUser, null=True, blank=False, related_name="message", on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    read = models.BooleanField(default=False)
    
    
    