import socket
import json
import threading
from board import Board

class SocketServer():
    def __init__(self, host="127.0.0.1", port="51419", format="utf-8"):
        self.HEADER_LEN = 16
        self.HOST=host
        self.PORT=port
        self.FORMAT=format
        self.server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn_dict={}
        self.board = Board(0.4)
    
    def bind(self):
        self.server.bind((self.HOST, self.PORT))
    
    def listen(self):
        self.server.listen()
    
    def accept(self):
        return self.server.accept()
    
    def close(self,conn, handler_id):
        conn.close()
        del self.conn_dict[handler_id]
    
    def send(self, msg_dict:dict[None], conn):
        message=json.dumps(msg_dict).encode(self.FORMAT)
        msg_length=len(message)
        send_length=str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER_LEN - len(send_length))
        conn.send(send_length)
        conn.send(message)
    
    def handler(self, conn, addr, handler_id):
        print(f"[UPDATE] New connection from: {addr}")
        connected=True
        while connected:
            msg_length = conn.recv(self.HEADER_LEN).decode(self.FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                tag = json.loads(conn.recv(msg_length).decode(self.FORMAT))["tag"]
                if tag == "CLOSE":
                    connected = False
                elif tag == "request_field":
                    pass
                elif tag == "click":
                    pass
                elif tag == "toggle_flag":
                    pass
                print(f"[{addr}] {tag}")
                #self.send("Msg received".encode(self.FORMAT), conn)
        self.close(conn, handler_id)
    
    def broadcast(self, msg_dict:dict[None]):
        for conn in self.conn_dict.values():
            self.send(msg_dict,conn)
        print("[BROADCAST] Broadcast")
    
    def start(self):
        self.listen()
        uuid=0
        print(f"[START] Started Listening on {self.HOST}")
        while True:
            try:
                conn, addr = self.server.accept()
                uuid+=1
                thread = threading.Thread(target=self.handler, args=(conn, addr, uuid))
                self.conn_dict[uuid]=conn
                thread.start()
                print(f"[UPDATE] Active Connection: {threading.activeCount() - 1}")
            except KeyboardInterrupt:
                break
        print("[CLOSE] Closed server.")