import json
from typing import Dict, Any, Callable

class SocketIOProtocol:
    def __init__(self):
        self.handlers: Dict[str, Callable] = {}
        
    async def handle_message(self, socket, message: str):
        try:
            data = json.loads(message)
            event = data.get('event')
            payload = data.get('data')
            
            if event in self.handlers:
                await self.handlers[event](socket, payload)
        except json.JSONDecodeError:
            print(f"Invalid message format: {message}")
            
    async def send(self, socket, event: str, data: Any):
        message = json.dumps({'event': event, 'data': data})
        await socket.send(message) 