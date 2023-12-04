import json
from django.db.models import Count
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Conversation, Message
from account.models import UserAccount


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'test'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

        self.send(text_data=json.dumps(
            {
                'type': 'connection_established',
                'message': 'You are now connected!'
            }
        ))

    # def receive(self, text_data=None,):
    #     print(text_data)
    #

    def receive(self, text_data=None, bytes_data=None):
        text_data = json.loads(text_data)
        message = text_data['message']
        sender_id = text_data['sender_id']
        receiver_id = text_data['receiver_id']
        users = [UserAccount.objects.get(pk=sender_id).id, UserAccount.objects.get(pk=receiver_id).id]
        conversation = Conversation.objects.filter(participants__in=users).annotate(
            participant_count=Count('participants')).filter(participant_count=len(users)).first()
        if not conversation:
            conversation = Conversation.objects.create()
            conversation.participants.add(*users)
        Message.objects.create(conversation=conversation, sender_id=sender_id, text=message)
        print('Message:', message)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {
                'type': 'chat_message',
                'message': message,
                'receiver_id': receiver_id,
                'sender_id': sender_id
            }
        )

        # self.send(text_data=json.dumps({
        #     'type': 'chat',
        #     'message': message
        # }))

    def chat_message(self, event):
        print(event, "kljklfjkljskljkljkljkljlk")
        message = event['message']
        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message,
            'receiver_id': event['receiver_id'],
            'sender_id': event['sender_id'],
            'dj': "dj"
        }))
