import socket
import json
from wordlist import arr as wordlist


def error_log(msg):
    print(f"[ERROR]: {msg}")


class Client:
    def __init__(self):
        self.HOST = "proj1.3700.network"
        self.PORT = 27993
        self.sock = None
        self.id = ""
        # does not exist -- network return val: 0
        self.greys = set()
        # exists but in different position to guess -- network return value: 1
        self.oranges = {}
        self.guess = None
        self.game_over = False
        self.guess_history = set()
        self.startConnection()

    def __del__(self):
        assert isinstance(self.sock, socket.socket), "Socket Initialization failed"
        print("[CLOSING]")
        self.sock.close()

    def initSocket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.HOST, self.PORT))

    def startConnection(self):
        self.initSocket()
        assert isinstance(self.sock, socket.socket), "Socket Initialization failed"
        payload = {"type": "hello", "northeastern_username": "kothandaraman.k"}
        data = json.dumps(payload) + '\n'
        print(f"[SENDING] {data}")
        self.sock.sendall(bytes(data, encoding="utf-8"))
        resp = json.loads(self.get_resp())

        if resp["type"] == "error":
            error_log(resp["message"])

        else:
            self.id = resp["id"]
            print(f"[RECEIVED] id: {self.id}")
            while not self.game_over:
                self.play()

    def is_possible_guess(self, word):
        # word has letter that is a grey
        for letter in word:
            if letter in self.greys:
                return False

        # word does not have a green in same position
        for i in range(len(self.guess)):
            if self.guess[i] != '-' and self.guess[i] != word[i]:
                return False

        # word has a letter in orange and at same position as seen before
        for i in range(len(word)):
            if word[i] in self.oranges and i in self.oranges[word[i]]:
                return False

        return True

    def get_next_guess(self):
        for word in wordlist:
            if self.is_possible_guess(word) and word not in self.guess_history:
                return word

    def update_guess(self, history):
        self.guess = ['-', '-', '-', '-', '-']
        for guess in history:
            greens_and_greys = set()
            for i in range(len(guess["word"])):
                if guess["marks"][i] == 2:
                    self.guess[i] = guess["word"][i]
                    greens_and_greys.add(guess["word"][i])
                elif guess["marks"][i] == 1:
                    if guess["word"][i] in self.oranges:
                        self.oranges[guess["word"][i]].append(i)
                    else:
                        self.oranges[guess["word"][i]] = [i]
                    greens_and_greys.add(guess["word"][i])
                else:
                    if guess["word"][i] not in greens_and_greys:
                        self.greys.add(guess["word"][i])
            self.guess_history.add(guess["word"])

    def play(self):
        if self.guess:
            next_guess = self.get_next_guess()
        else:
            # initial guess because 3 vowels and 2 consonants
            next_guess = "about"

        payload = {"type": "guess", "id": self.id, "word": next_guess}
        data = json.dumps(payload) + '\n'
        print(f"[GUESSING] {data}")
        self.num_guesses += 1
        self.sock.sendall(bytes(data, encoding="utf-8"))
        resp = json.loads(self.get_resp())

        if resp["type"] == "error":
            error_log(resp["message"])
            self.game_over = True

        elif resp["type"] == "bye":
            print(f'[GAME OVER] secret flag: {resp["flag"]}')
            self.game_over = True

        else:
            self.update_guess(resp["guesses"])

    def get_resp(self):
        resp = ''
        while True:
            buf = self.sock.recv(1)
            if buf.decode("utf-8") == '\n':
                break
            resp += buf.decode("utf-8")
        return resp


if __name__ == "__main__":
    c = Client()
