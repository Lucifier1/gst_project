#  routing.py

from django.urls import re_path
from app_modules.chat import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<first_name>[\w.@+-]+)/$', consumers.ChatConsumer.as_asgi()),
]
