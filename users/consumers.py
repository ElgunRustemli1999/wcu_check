import json
from channels.generic.websocket import AsyncWebsocketConsumer

class FaceRecognitionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'face_recognition_group'

        # WebSocket otağına qoşuluruq
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # WebSocket otağından çıxırıq
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        face_data = text_data_json.get("face_data")

        # Üz məlumatlarını emal edirik (simulyasiya edilmiş cavab)
        response = {
            "status": "success",
            "message": "Face data received and processed."
        }

        # WebSocket-ə cavab göndəririk
        await self.send(text_data=json.dumps(response))
