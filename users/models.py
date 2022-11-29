import uuid 

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


#CustomUser = get_user_model()

     
class CustomUser(AbstractUser):
    
    secondary_id = models.UUIDField(default=uuid.uuid4, editable=False)
    email = models.EmailField(_('email address'), blank=False, null=False, unique=True)
    #bio = models.CharField(max_length=1000, null=True, blank=True)
    #profile_pic = models.ImageField(null=True, blank=True)
    connections = models.ManyToManyField("self", blank=True)
    
    def __str__(self):
        return self.email 
        
        
class ConnectionRequest(models.Model):
    
    secondary_id = models.UUIDField(default=uuid.uuid4, editable=False)
    is_accepted = models.BooleanField(default=False)
    sender = models.ForeignKey(CustomUser, related_name="sent_requests", on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name="received_requests", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-id']