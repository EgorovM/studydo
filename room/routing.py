from django.urls import re_path
from django.conf import settings

from . import consumers

dom = 'ws' + 's' * settings.IS_HOST

websocket_urlpatterns = [
    re_path(r'%s/chat/(?P<room_name>\w+)/$' % dom, consumers.ChatConsumer.as_asgi()),
    re_path(r'%s/tasks/(?P<room_name>\w+)/$' % dom, consumers.TasksConsumer.as_asgi()),
    re_path(r'%s/board/(?P<room_name>\w+)/$' % dom, consumers.BoardConsumer.as_asgi()),
]
