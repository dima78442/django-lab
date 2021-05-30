import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.forms.models import model_to_dict
import datetime
from webapp.models import ConnectedUsers, Person, Phone


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.person_id = self.scope['url_route']['kwargs']['person_id']
        self.person_group_name = 'chat_%s' % self.person_id

        async_to_sync(self.channel_layer.group_add)(
            self.person_group_name,
            self.channel_name
        )

        username = f"Anonymous - {self.scope['client'][1]}" \
            if self.scope['user'].username == "" else self.scope['user'].username
        ConnectedUsers.objects.create(first_name=username)
        self.username = username
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.person_group_name,
            self.channel_name
        )
        ConnectedUsers.objects.filter(first_name=self.username).delete()

    # Receive message from WebSocket
    def receive(self, text_data):
        data_json = json.loads(text_data)

        person = Person.objects.get(id=int(data_json['person_id']))
        p = Phone(person=person, phone_number=data_json['phone_number'], active=data_json['active'])
        p.save()

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.person_group_name,
            {
                'type': 'chat_message',
                'entity_data': data_json
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        entity_data = event['entity_data']
        print(entity_data)
        # Send message to WebSocket
        self.send(text_data=json.dumps(entity_data))


class TasksConsumer(WebsocketConsumer):
    def connect(self):
        self.group_name = "finished_tasks"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        print("connect")
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        print("disconnect")
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def receive(self, text_data):
        print("receive")
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(text_data_json)
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'task_message',
                'message': message
            }
        )

    def task_message(self, event):
        print("task_message")
        message = event['message']
        print(message)

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
