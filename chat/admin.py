from django.contrib import admin

from .models import Inbox, Message


admin.site.register(Inbox)
admin.site.register(Message)
