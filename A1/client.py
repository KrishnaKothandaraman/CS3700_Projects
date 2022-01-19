import socket
import json
from wordlist import arr


def error_log(msg):
    print(f"[ERROR]: {msg}")


class Client:
    def __init__(self):
        self.HOST = "proj1.3700.network"
        self.PORT = 27993
        self.s = None
        self.id = ""
        self.startConnection()

    def __del__(self):
        assert isinstance(self.s, socket.socket), "Socket Initialization failed"
        print("[CLOSING]")
        self.s.close()

    def initSocket(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.HOST, self.PORT))

    def startConnection(self):
        self.initSocket()
        assert isinstance(self.s, socket.socket), "Socket Initialization failed"
        payload = {"type": "hello", "northeastern_username": "kothandaraman.k"}
        data = json.dumps(payload) + '\n'
        print(f"[SENDING] {data}")
        self.s.sendall(bytes(data, encoding="utf-8"))
        resp = json.loads(self.getresp())

        if resp["type"] == "error":
            error_log(resp["message"])

        else:
            self.id = resp["id"]
            print(f"[RECEIVED] id: {self.id}")
            self.play()

    def play(self):
        print("[PLAYING]")

    def getresp(self):
        resp = ''
        while True:
            buf = self.s.recv(1)
            if buf.decode("utf-8") == '\n':
                break
            resp += buf.decode("utf-8")
        return resp


if __name__ == "__main__":
    c = Client()
