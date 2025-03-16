import socket
import json

class SocketClient():
    def __init__(self, host="127.0.0.1", port="51419", format="utf-8"):
        self.HEADER_LEN = 16
        self.HOST=host
        self.PORT=port
        self.FORMAT=format
        self.client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def connect(self):
        self.client.connect((self.HOST, self.PORT))
    
    def send(self, msg_dict:dict[None])-> dict:
        message=json.dumps(msg_dict).encode(self.FORMAT)
        msg_length=len(message)
        send_length=str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER_LEN - len(send_length))
        self.client.send(send_length)
        self.client.send(message)
        return json.loads(self.client.recv(2048).decode(self.FORMAT))
    
    def send_click(self):
        pass
    
    def send_toggle_flag(self):
        pass
    
    def send_request_field(self):
        field=self.send({"tag":"request_field", "data":{"start_coord":[0,0], "end_coord":[2,4]}})