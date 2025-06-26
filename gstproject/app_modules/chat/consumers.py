import json
from channels.layers import get_channel_layer
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from app_modules.adminapp.models import User
import base64
from io import BytesIO
from PIL import Image
from app_modules.chat.models import DirectChat, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Retrieve the room name from the URL (e.g. /chat/room_name/)
        self.first_name = self.scope['url_route']['kwargs']['first_name']
        self.room_group_name = f'chat_{self.first_name}'
        self.user = self.scope['user']

        self.chat_room, _ = DirectChat.objects.get_or_create(
            user1=self.user, user2__username=self.first_name
        )
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Accept WebSocket connection 
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Handles receiving messages from WebSocket.
        text_data will be a JSON object containing the message and type.
        """

        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        message_type = text_data_json.get('type', 'text')  # Text or media

        # Handle the message type
        if message_type == 'text':
            await self.handle_text_message(message)
        elif message_type == 'media':
            await self.handle_media_message(message)

    async def handle_text_message(self, message):
        """
        Handle text messages and send them to the room group.
        """

        # You can save the message to the database here if necessary
        user = self.scope['user']  # Get the user who sent the message

        chat_room = DirectChat.objects.get_or_create(user1=user,user2__username=self.first_name)  # Fetch the chat room
        new_message = Message.objects.create(room=chat_room, sender=user, content=message)

        # Broadcast the message to all group members
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': user.first_name,
                'message_type': 'text',
            }
        )

    async def handle_media_message(self, media_data):
        """
        Handle media messages (e.g., image or file).
        """
        user = self.scope['user']
        
        # Process the media data (base64 encoded image, file, etc.)
        try:
            # Decode the media file if it's a base64 string (for example image)
            media_content = base64.b64decode(media_data)
            
            # Optionally save the media content to a file or media folder
            # This is an example for an image
            image = Image.open(BytesIO(media_content))
            media_file_path = f"media/chat/{user.first_name}_image.jpg"
            image.save(media_file_path)

            # Save media message
            chat_room = DirectChat.objects.get_or_create(user1=user,user2=self.first_name)
            new_message = Message.objects.create(room=chat_room, sender=user, media_file=media_file_path)

            # Send the media message to the group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': media_file_path,  # You could send a media URL/path
                    'sender': user.first_name,
                    'message_type': 'media',
                }
            )
        except Exception as e:
            print(f"Error handling media message: {e}")

    async def chat_message(self, event):
        """
        Receives a message from the WebSocket group and sends it to the client.
        """
        message = event['message']
        sender = event['sender']
        message_type = event['message_type']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'message_type': message_type,
        }))
        