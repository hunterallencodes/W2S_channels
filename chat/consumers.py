import json
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.consumer import SyncConsumer
from django.contrib.auth import get_user_model

from .models import Thread

User = get_user_model()


class ChatConsumer(SyncConsumer):
    async def connect(self):
        me = ['user']
        other_username = self.scope['url_route']['kwargs']['username']
        other_user = User.objects.get(username=other_username)
        thread_obj = Thread.objects.get_or_create_personal_thread(me, other_user)
        self.room_name = f'personal_thread_{thread_obj.id}'
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = text_data_json['user']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': user,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        user = event['user']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user': user,
        }))

    @database_sync_to_async
    def get_user(self):
        return User.objects.get()