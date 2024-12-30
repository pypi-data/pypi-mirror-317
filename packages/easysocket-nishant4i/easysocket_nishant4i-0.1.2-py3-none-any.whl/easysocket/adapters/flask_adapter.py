from flask import request
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
import uuid
import asyncio

class FlaskAdapter:
    def __init__(self, app, easysocket, path):
        self.app = app
        self.easysocket = easysocket
        self.path = path
        self.setup_routes()
        
    def setup_routes(self):
        @self.app.route(self.path)
        async def websocket():
            if request.environ.get('wsgi.websocket'):
                ws = request.environ['wsgi.websocket']
                client_id = str(uuid.uuid4())
                self.easysocket.clients[client_id] = ws
                
                try:
                    while not ws.closed:
                        message = ws.receive()
                        if message:
                            await self.easysocket.protocol.handle_message(ws, message)
                except Exception as e:
                    print(f"WebSocket error: {e}")
                finally:
                    if client_id in self.easysocket.clients:
                        del self.easysocket.clients[client_id]
                        
            return ''
        
    def run(self, host='0.0.0.0', port=5000):
        server = WSGIServer((host, port), self.app, handler_class=WebSocketHandler)
        server.serve_forever()
