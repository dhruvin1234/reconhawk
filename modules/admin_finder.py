import requests
from queue import Queue
import threading
from colorama import Fore, Style

# Default wordlist (can be customized)
DEFAULT_WORDLIST = [
    "admin",
    "admin/login",
    "adminpanel",
    "administrator",
    "dashboard",
    "cpanel",
    "admin_area",
    "admin1",
    "login",
    "manage",
    "controlpanel",
    "backend",
    "wp-admin",
    "wp-login.php",
    "wp-content",
    "wp-includes",
    "wp-login",
    "wp-admin.php",
    "joomla-admin",
    "admin.php",
    "admin_area",
    "userlogin",
    "signin",
    "signin.php",
    "admin-login",
    
]

def worker(url, queue, total_paths):
    while not queue.empty():
        path = queue.get()
        target_url = f"{url.rstrip('/')}/{path}"

        try:
            response = requests.get(target_url, timeout=5)
            if response.status_code == 200:
                print(f"{Fore.RED}[200] Found: {target_url}{Style.RESET_ALL}")
            elif response.status_code == 403:
                print(f"{Fore.MAGENTA}[403] Forbidden: {target_url}{Style.RESET_ALL}")
        except requests.RequestException:
            pass
        finally:
            worker.completed += 1
            print(f"{Fore.CYAN}Progress: {worker.completed}/{total_paths} paths completed{Style.RESET_ALL}", end='\r')
            queue.task_done()

def admin_finder_main(url, wordlist_path=None, thread_count=10):
    # Use default wordlist if no custom wordlist is provided
    if wordlist_path:
        try:
            with open(wordlist_path, 'r') as file:
                paths = file.read().splitlines()
        except FileNotFoundError:
            print(f"{Fore.RED}[-] Wordlist not found!{Style.RESET_ALL}")
            return
    else:
        paths = DEFAULT_WORDLIST

    print(f"{Fore.YELLOW}[+] Starting Admin Panel Finder...{Style.RESET_ALL}")
    q = Queue()
    for path in paths:
        q.put(path)

    total_paths = len(paths)
    worker.completed = 0

    print(f"{Fore.YELLOW}[+] Total paths to try: {total_paths}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[+] Using {thread_count} threads{Style.RESET_ALL}\n")

    threads = []
    for _ in range(thread_count):
        t = threading.Thread(target=worker, args=(url, q, total_paths))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print(f"\n{Fore.GREEN}[+] Admin Panel Search Finished!{Style.RESET_ALL}")
