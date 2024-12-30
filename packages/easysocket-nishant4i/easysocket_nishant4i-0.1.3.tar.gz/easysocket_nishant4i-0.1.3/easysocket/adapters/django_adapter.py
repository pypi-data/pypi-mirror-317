from channels.generic.websocket import AsyncWebsocketConsumer
import uuid

class DjangoAdapter(AsyncWebsocketConsumer):
    def __init__(self, easysocket):
        super().__init__()
        self.easysocket = easysocket
        self.client_id = None
        
    async def connect(self):
        self.client_id = str(uuid.uuid4())
        self.easysocket.clients[self.client_id] = self
        await self.accept()
        
    async def disconnect(self, close_code):
        if self.client_id in self.easysocket.clients:
            del self.easysocket.clients[self.client_id]
            
    async def receive(self, text_data):
        await self.easysocket.protocol.handle_message(self, text_data)
        
    async def send_message(self, event, data):
        await self.easysocket.protocol.send(self, event, data) 