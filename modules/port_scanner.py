import socket
import threading
import queue
from colorama import Fore, Style

def scan_ports(target, start_port, end_port, thread_no):
    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print("[-] Host resolution failed.")
        return

    print(f"\n{Fore.YELLOW}[+] Scanning target: {target_ip}\n")

    q = queue.Queue()
    open_ports = []

    for port in range(start_port, end_port + 1):
        q.put(port)

    def scan_port():
        while not q.empty():
            port = q.get()
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)
                result = s.connect_ex((target_ip, port))
                if result == 0:
                    banner = grab_banner(s)
                    open_ports.append((port, banner))
                s.close()
            except:
                pass
            q.task_done()

    def grab_banner(sock):
        try:
            return sock.recv(1024).decode().strip()
        except:
            return ""

    threads = []
    for _ in range(thread_no):
        t = threading.Thread(target=scan_port)
        t.daemon = True
        t.start()
        threads.append(t)

    q.join()

    print(f"{Fore.RED}PORT\tSTATE\tSERVICE")
    for port, banner in sorted(open_ports):
        service = get_service_name(port)
        print(f"{Fore.RED}{port}/tcp\topen\t{service} {f'| {banner}' if banner else ''}")

def get_service_name(port):
    try:
        return socket.getservbyport(port)
    except:
        return "unknown"
