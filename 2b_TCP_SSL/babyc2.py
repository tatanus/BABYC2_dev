import socket
import ssl
import subprocess
import os
import select

HOST = "127.0.0.1"
PORT = 9999
CERT_FILE = "server.pem"

def is_socket_valid(socket):
    readable, writable, exceptional = select.select([socket], [], [], 0)
    if not readable:
        return True
    return False

def generate_certificate(cert_file):
    # Check if certificate file exists
    if not os.path.exists(cert_file):
        # Generate a self-signed certificate
        os.system(f"openssl req -x509 -newkey rsa:4096 -keyout {cert_file} -out {cert_file} -days 365 -nodes -subj '/CN=localhost'")

def cmd_loop(session):
    while True:
        if not is_socket_valid(session):
            break
        command = input(f"Session > ")
        command = f'{command}'  # Wrap command in quotes
        session.sendall(command.encode('utf-8') + b"\n")
        data = session.recv(1024).decode()
        if data:
            response_lines = data.split('\n')
            for line in response_lines:
                print(f"{line}")

def main():
    # Create a self-signed SSL certificate
    generate_certificate(CERT_FILE)

    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.check_hostname = False
    ssl_context.load_cert_chain(CERT_FILE)

    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    listener.bind((HOST, PORT))
    listener.listen()
    mysocket, addr = listener.accept()

    mysslsocket = ssl_context.wrap_socket(mysocket, server_side=True)
    cmd_loop(mysslsocket)


if __name__ == "__main__":
    main()
