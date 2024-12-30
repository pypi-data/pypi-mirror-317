import json
from typing import Dict, Any, Callable

class WebSocketProtocol:
    def __init__(self):
        self.handlers: Dict[str, Callable] = {}
        
    async def handle_message(self, websocket, message: str):
        try:
            data = json.loads(message)
            event = data.get('event')
            payload = data.get('data')
            
            if event in self.handlers:
                await self.handlers[event](websocket, payload)
        except json.JSONDecodeError:
            print(f"Invalid message format: {message}")
            
    async def send(self, websocket, event: str, data: Any):
        message = json.dumps({'event': event, 'data': data})
        await websocket.send(message) 