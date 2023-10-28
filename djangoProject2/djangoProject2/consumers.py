from channels.exceptions import StopConsumer
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def websocket_connect(self, message):
        self.accept()

    def websocket_receive(self, message):
        print(message)
        self.send("不要")

    def websocket_disconnect(self, message):
        raise StopConsumer()
