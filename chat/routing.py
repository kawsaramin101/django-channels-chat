from django.urls import re_path, path

from . import consumers


websocket_urlpatterns = [
    #re_path(r"ws/livefeed/(?P<match_id>\w+)/$", consumers.LiveFeedConsumer.as_asgi()),
    path("ws/inbox/<str:inbox_secondary_id>/", consumers.InboxConsumer.as_asgi()),
]
