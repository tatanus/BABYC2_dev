import paramiko
import socket
import threading
import sys

HOST = "127.0.0.1"
PORT = 9999
USERNAME = "user"
PASSWORD = "password"

# Define the SSH server key
HOST_KEY = paramiko.RSAKey.generate(2048)

class SSHServer(paramiko.ServerInterface):
    def __init__(self, server_username, server_password):
        self.server_username = server_username
        self.server_password = server_password
        self.event = threading.Event()
    def check_auth_password(self, username, password):
        if username == self.server_username and password == self.server_password:
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED
    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

def client_handler(client_socket, username, password, server_host_key):
    try:
        #bind client socket to ssh server session and add rsa key
        ssh_session = paramiko.Transport(client_socket)
        ssh_session.add_server_key(server_host_key)
        server = SSHServer(username, password)

        #start the ssh server and negotiate ssh params
        try:
            ssh_session.start_server(server=server)
        except SSHException as err:
            print("[!] SSH Parameters Negotiation Failed")

        print("[*] SSH Parameters Negotiation Succeeded")

        #authenticate the client
        print("[*] Authenticating")
        ssh_channel = ssh_session.accept(20)
        if ssh_channel == None or not ssh_channel.active:
            print("[*] SSH Client Authentication Failure")
            ssh_session.close()
        else:
            print("[*] SSH Client Authenticated")

            #ssh channel is established. We can start the shell
            #and send commands from input
            while not ssh_channel.closed:
                command = input(f"Session > ").rstrip()
                if len(command):
                    if command != "exit":
                        ssh_channel.send(command)
                        print(ssh_channel.recv(1024).decode('utf-8') + '\n')
                    else:
                        print("[*] Exiting")
                        try:
                            ssh_session.close()
                        except:
                            print("[!] Error closing SSH session")
                        print("[*] SSH session closed")
    except Exception as err:
        print("[*] Caught Exception: ", str(err))
        print("[*] Exiting Script")
        try:
            ssh_session.close()
        except:
            print("[!] Error closing SSH session")

        print("[*] SSH session closed")
        sys.exit(1)

def main():
    if len(sys.argv) == 3:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        username = sys.argv[3]
        password = sys.argv[4]
    else:
        server_address = HOST
        server_port = PORT
        username = USERNAME
        password = PASSWORD

    # Create a socket and listen for incoming connections
    try:
        #server_host_key = paramiko.RSAKey(filename="ch2_ssh_server.key")
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((server_address, server_port))
        listener.listen(100)
    except:
        print(f"[!] Bind Error for SSH Server using {server_address}")
        sys.exit(1)

    print(f"Listening for connections on {server_address}:{server_port}")

    while True:
        client_socket, addr = listener.accept()
        print(f"SSH connection from {addr}")
        client_handler(client_socket, username, password, HOST_KEY)

if __name__ == "__main__":
    main()
