import asyncio
import websockets
from typing import Callable, Dict, List

class EasySocket:
    def __init__(self, app, path='/ws'):
        self.app = app
        self.path = path
        self.clients = {}
        self.handlers = {}
        self._setup_server()
    
    def _setup_server(self):
        """Configure WebSocket server based on framework"""
        if hasattr(self.app, 'route'):  # Flask
            self._setup_flask()
        else:  # Django
            self._setup_django()
    
    def on(self, event_name: str) -> Callable:
        """Decorator for registering event handlers"""
        def decorator(handler):
            self.handlers[event_name] = handler
            return handler
        return decorator
    
    async def broadcast(self, event: str, data: dict):
        """Send message to all connected clients"""
        message = {'event': event, 'data': data}
        for client in self.clients.values():
            await client.send(message)
    
    async def send_to(self, client_id: str, event: str, data: dict):
        """Send message to specific client"""
        if client_id in self.clients:
            message = {'event': event, 'data': data}
            await self.clients[client_id].send(message)
