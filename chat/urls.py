from django.urls import path

from .views import index, chat

app_name = "chat"

urlpatterns = [
    path('', index, name="index"),
    path('inbox/<str:inbox_secondary_id>/', chat, name="inbox"),
    
]