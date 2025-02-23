# messaging/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import mysql.connector
from django.conf import settings

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f'chat_{self.conversation_id}'

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

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender_type = text_data_json['sender_type']
        sender_id = text_data_json['sender_id']

        # Save message to database
        message_id = await self.save_message(
            conversation_id=self.conversation_id,
            content=message,
            sender_type=sender_type,
            sender_id=sender_id
        )

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_type': sender_type,
                'sender_id': sender_id,
                'message_id': message_id
            }
        )

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender_type': event['sender_type'],
            'sender_id': event['sender_id'],
            'message_id': event['message_id']
        }))

    @database_sync_to_async
    def save_message(self, conversation_id, content, sender_type, sender_id):
        db = mysql.connector.connect(
            host=settings.DATABASES['default']['HOST'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            database=settings.DATABASES['default']['NAME']
        )
        cursor = db.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO Messages (conversation_id, content, sender_type, sender_id, is_read)
                VALUES (%s, %s, %s, %s, FALSE)
            """, (conversation_id, content, sender_type, sender_id))
            
            message_id = cursor.lastrowid
            
            cursor.execute("""
                UPDATE Conversations 
                SET updated_at = CURRENT_TIMESTAMP 
                WHERE id = %s
            """, (conversation_id,))
            
            db.commit()
            return message_id
        finally:
            cursor.close()
            db.close()

