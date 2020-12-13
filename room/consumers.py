import bs4
import json
import random
import requests

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        type = 'text' if not 'type' in text_data_json else text_data_json['type']
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message_type': type,
                'message': message
            }
        )

    def chat_message(self, event):
        message = event['message']
        type = event['message_type']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message_type': type,
            'message': message
        }))


class TasksConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'tasks_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        tasks = self.get_tasks()

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'tasks': tasks
            }
        )

    def chat_message(self, event):
        message = event['tasks']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'tasks': message
        }))


    def get_tasks(self):
        test_ids = [35516816, 35517054]
        url = 'https://ege.sdamgia.ru/test?id=%s&nt=True&pub=False'
        r = requests.get(url % random.choice(test_ids))
        soup = bs4.BeautifulSoup(r.content)
        c = soup.find_all('div', {'class': 'prob_view'})[1]

        html = ''

        for c in soup.find_all('div', {'class': 'prob_view'}):
            html += str(c).replace('src="/', 'src="https://ege.sdamgia.ru/')

        return html
