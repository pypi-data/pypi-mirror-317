class EasySocketClient {
    constructor(url) {
        this.socket = new WebSocket(url);
        this.handlers = {};
        
        this.socket.onmessage = (event) => {
            const { event: eventName, data } = JSON.parse(event.data);
            if (this.handlers[eventName]) {
                this.handlers[eventName](data);
            }
        };
    }

    on(event, handler) {
        this.handlers[event] = handler;
    }

    send(event, data) {
        this.socket.send(JSON.stringify({ event, data }));
    }
} 