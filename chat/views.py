from django.shortcuts import render

from .models import Inbox


def index(request):
    
    inboxes = request.user.inboxes.all()
    
    context = {
        "inboxes": inboxes
    }
    
    return render(request, "chat/index.html", context)
    
    
    
def chat(request, inbox_secondary_id):
    
    inbox = Inbox.objects.prefetch_related("participants").get(secondary_id=inbox_secondary_id)
    inbox_name = inbox.name(request.user.id) 
    messages = inbox.messages.all() 
    
    if not request.user in inbox.participants.all():
        return 
    
    context = {
        "inbox": inbox,
        "inbox_name": inbox_name,
        "messages": messages,
    }
    
    return render(request, "chat/inbox.html", context)
    
    
    