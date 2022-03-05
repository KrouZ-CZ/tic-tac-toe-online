import random
import socket
import threading
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 2000))

server.listen()
find_game = []

class User:
    def __init__(self, user, adres):
        self.user = user
        self.adres = adres
        print(f'Connected: {adres}')
        self.liss()
    def liss(self):
        try:
            self.data = self.user.recv(1024).decode('utf-8')
            if self.data == 'FindGame':
                find_game.append(self.user)
                check_game()
        except:
            print(f'Disconnected: {self.adres}')
    def send(self, r):
        self.user.send(r.encode('utf-8'))
class Game:
    def __init__(self, usr1, usr2):
        self.win = 0
        self.user1 = usr1
        self.user2 = usr2
        usr1.send('1'.encode('utf-8'))
        usr2.send('0'.encode('utf-8'))
        self.start = random.randint(1, 2)
        self.pole = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.stop = False
        while not self.stop:
            self.check_win()
            if self.win != 0:
                match self.start:
                    case 1: 
                        self.user1.send('loose'.encode('utf-8'))
                        self.user2.send('win'.encode('utf-8'))
                    case 2: 
                        self.user1.send('win'.encode('utf-8'))
                        self.user2.send('loose'.encode('utf-8'))
                break
            self.next = False
            match self.start:
                case 1: 
                    self.user1.send('1'.encode('utf-8'))
                    self.user2.send('0'.encode('utf-8'))
                case 2: 
                    self.user1.send('0'.encode('utf-8'))
                    self.user2.send('1'.encode('utf-8'))
            self.user1.send(str(self.pole).encode('utf-8'))
            self.user2.send(str(self.pole).encode('utf-8'))
            match self.start:
                case 1: self.check1()
                case 2: self.check2()
            self.move()
            if self.next == True:
                self.start = 2 if self.start == 1 else 1
        print('game stop')
    def check1(self):
        try:
            self.data = self.user1.recv(1024).decode('utf-8')
        except:
            self.sos()
    def check2(self):
        try:
            self.data = self.user2.recv(1024).decode('utf-8')
        except:
            self.sos()
    def move(self):
        try:
            if self.pole[int(self.data)] == 0:
                self.pole[int(self.data)] = self.start
                self.next = True
        except: 
            pass
    def sos(self):
        try:
            try:
                self.user1.send('exit'.encode('utf-8'))
                self.user2.send('exit'.encode('utf-8'))
            except:
                self.user2.send('exit'.encode('utf-8'))
                self.user1.send('exit'.encode('utf-8'))
        except:
            pass
        self.stop = True
    def check_win(self):
        if self.pole[0] != 0 and self.pole[0] == self.pole[1] == self.pole[2]: self.win = self.pole[0]
        if self.pole[3] != 0 and self.pole[3] == self.pole[4] == self.pole[5]: self.win = self.pole[3]
        if self.pole[6] != 0 and self.pole[6] == self.pole[7] == self.pole[8]: self.win = self.pole[6]

        if self.pole[0] != 0 and self.pole[0] == self.pole[3] == self.pole[6]: self.win = self.pole[0]
        if self.pole[1] != 0 and self.pole[1] == self.pole[4] == self.pole[7]: self.win = self.pole[1]
        if self.pole[2] != 0 and self.pole[2] == self.pole[5] == self.pole[8]: self.win = self.pole[2]

        if self.pole[0] != 0 and self.pole[0] == self.pole[4] == self.pole[8]: self.win = self.pole[0]
        if self.pole[6] != 0 and self.pole[6] == self.pole[4] == self.pole[2]: self.win = self.pole[6]
def check_game():
    global find_game
    if len(find_game) >= 2:
        print('Game started')
        temp = find_game
        find_game = []
        Game(temp[0], temp[1])
    else:
        while len(find_game) == 0:
            pass
def main():
    while True:
        print('Checking...')
        user, adres = server.accept()
        t = threading.Thread(target=User, args=(user, adres))
        t.start()
if __name__ == "__main__":
    main()
