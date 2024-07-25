# Spyware

## Introduction

Welcome to the Spyware project, a client-server application designed for educational purposes to demonstrate real-time data collection and transmission from users' devices. This project combines various technologies to create a platform for understanding how spyware can operate.

**Disclaimer: This project is for educational purposes only. Unauthorized use of spyware is illegal and unethical. Always obtain proper consent before monitoring any device.**

## Features

- **Real-Time Screen Sharing:** The project provides real-time screen sharing, enabling the attacker to see the target's screen instantly. This feature ensures continuous monitoring of the target's activities.

- **Real-Time Keylogger:** The spyware includes a real-time keylogger that captures and logs all keystrokes made by the target. This allows the attacker to see everything the target types, including passwords, messages, and other sensitive information.

- **Multi-Attacker Support:** Multiple attackers can connect to the same target simultaneously. This feature allows collaborative monitoring and data collection from the target.

- **Sending Keystrokes:** The spyware allows attackers to send keystrokes to the target's machine, enabling remote control and interaction with the target's system.

## Getting Started

1. **Clone the Repository:** Clone the project repository to your local machine.

2. **Requirements:** Copy the contents of `requirements.txt` and paste it into the terminal.

3. **Server Setup:**  Copy the path to the `server.py` and paste it into the terminal like this: <br> `python PATH\server.py`<br> If you wish, you can set your own Port like this: <br> `python PATH\server.py <PORT>`<br> Otherwise the Port will be automatically set to 2000.

4. **Target Setup:** Copy the path to the `target.py` and paste it into the terminal like this: <br> `python PATH\target.py`<br> If you wish, you can set your own IP and/or Port like this: <br> `python PATH\target.py <IP> <PORT>`<br> Otherwise the IP and/or Port will be automatically set to 127.0.0.1(IP) and/or 2000(Port)
   
5. **Attacker Setup:** Copy the path to the `attacker.py` and paste it into the terminal like this: <br> `python PATH\attacker.py`<br> If you wish, you can set your own IP and/or Port like this: <br> `python PATH\attacker.py <IP> <PORT>`<br> Otherwise the IP and/or Port will be automatically set to 127.0.0.1(IP) and/or 2000(Port)
