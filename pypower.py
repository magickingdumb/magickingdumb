import socket
import ssl
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

# Configuration
target_ip = "[Add URL Here]"
ports_to_scan = [80, 443]
timeout_seconds = 100
max_threads = 50

# Functions
def scan_port(port):
    try:
        if port == 80:
            handle_http_port(port)
        elif port == 443:
            handle_https_port(port, timeout_seconds)
    except Exception as e:
        print(f"[!] Error interacting with port {port}: {str(e)}")

def handle_http_port(port):
    response = ""
    with socket.create_connection((target_ip, port), timeout=timeout_seconds) as sock:
        sock.sendall(b"GET / HTTP/1.1\r\nHost: " + target_ip.encode() + b"\r\nConnection: close\r\n\r\n")
        response = receive_response(sock)
    print_response(port, response)

def handle_https_port(port, timeout):
    context = ssl.create_default_context()
    with socket.create_connection((target_ip, port), timeout=timeout) as sock:
        with context.wrap_socket(sock, server_hostname=target_ip) as ssock:
            ssock.settimeout(timeout)
            ssock.sendall(b"GET / HTTP/1.1\r\nHost: " + target_ip.encode() + b"\r\nConnection: close\r\n\r\n")
            response = receive_response(ssock)
    print_response(port, response)

def receive_response(sock):
    response = ""
    try:
        while True:
            chunk = sock.recv(4096).decode('utf-8', 'ignore')
            if not chunk:
                break
            response += chunk
    except socket.timeout:
        print(f"[!] Timeout while receiving data from port {sock.getpeername()[1]}")
    return response

def print_response(port, response):
    if response:
        print(f"[+] Port {port} is open. Response received:")
        lines = response.splitlines()
        for line in lines:
            print(f"    [>] {line}")
    else:
        print(f"[+] Port {port} is open but no data received.")

# Main execution
if __name__ == "__main__":
    print("[*] Starting advanced scan...")
    start_time = datetime.now()
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        executor.map(scan_port, ports_to_scan)
    end_time = datetime.now()
    print(f"[*] Advanced scan completed in {(end_time - start_time).total_seconds()} seconds.")
