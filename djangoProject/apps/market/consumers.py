import json
from channels.generic.websocket import AsyncWebsocketConsumer


class StockPriceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # You could use a group name for broadcasting updates.
        self.group_name = "stock_updates"
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        # Process data if needed
        # For now, just echo the message back:
        await self.send(text_data=json.dumps({
            'message': data.get('message', '')
        }))

    # Receive message from group
    async def stock_update(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))