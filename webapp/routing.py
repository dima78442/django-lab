from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    path('ws/lab/tasks/', consumers.TasksConsumer.as_asgi()),
    re_path(r'ws/lab/(?P<person_id>\w+)/$', consumers.ChatConsumer.as_asgi())
]
