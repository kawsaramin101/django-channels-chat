import json

from django.template.loader import render_to_string 

from asgiref.sync import sync_to_async

from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .models import Inbox, Message


ACTIONS = ["send_message"]

class InboxConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.inbox_secondary_id = self.scope["url_route"]["kwargs"]["inbox_secondary_id"]
        self.inbox_group_id = "inbox_%s" % self.inbox_secondary_id
        self.user = self.scope["user"]
        
        self.inbox = await Inbox.objects.prefetch_related("participants").aget(secondary_id=self.inbox_secondary_id)
        
        if self.user.is_authenticated and self.user in self.inbox.participants.all():
            await self.channel_layer.group_add(self.inbox_group_id, self.channel_name)
            await self.accept()
        else:
            await self.close()
        
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.inbox_group_id, self.channel_name)
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json.get("action")
        data = text_data_json.get("data")
        
        if not action in ACTIONS:
            return
        await self.channel_layer.group_send(
            self.inbox_group_id, {"type": action, "data": data}
        )
        
    async def send_message(self, event):
        data = event.get("data")
        data["inbox"] = self.inbox 
        data["sender"] = self.user
        message = await Message.objects.acreate(**data)
        
        context = {
            "user": self.user,
            "message": message,
        }
        rendered_message = await sync_to_async(render_to_string)('chat/partials/message-partial.html', context)
        
        await self.send(text_data=json.dumps({
            "action": "add_message", 
            "rendered_message": rendered_message, 
            "sender_secondary_id": str(message.sender.secondary_id), 
            "message_secondary_id": str(message.secondary_id), 
        }))

        

