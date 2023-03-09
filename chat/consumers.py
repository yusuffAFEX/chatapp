import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, code):
        # Leave the group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from websocket
    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to the group
        await self.channel_layer.group_send(self.room_group_name, {"type": "chat_message", "message": message})

    # Receive message from the group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to Websocket
        await self.send(text_data=json.dumps({"message": message}))
