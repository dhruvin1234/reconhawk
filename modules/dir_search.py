import requests
import threading
from queue import Queue
from colorama import Fore, Style

def worker(url, extension, queue, total_words, lock):
    while not queue.empty():
        word = queue.get()
        if extension and not word.endswith(extension):
            word = word + extension
        target_url = f"{url.rstrip('/')}/{word}"

        try:
            response = requests.get(target_url, timeout=5)
            if response.status_code == 200:
                with lock:
                    print(f"{Fore.GREEN}[200] Found: {target_url}{Style.RESET_ALL}")
            elif response.status_code == 403:
                with lock:
                    print(f"{Fore.MAGENTA}[403] Forbidden: {target_url}{Style.RESET_ALL}")
        except requests.RequestException:
            pass
        finally:
            with lock:
                worker.completed += 1
                print(f"{Fore.CYAN}[*] Progress: {worker.completed}/{total_words} words completed{Style.RESET_ALL}", end='\r')
            queue.task_done()

def directory_search(url, wordlist_path, thread_count):
    try:
        with open(wordlist_path, 'r') as file:
            words = file.read().splitlines()
    except FileNotFoundError:
        print(f"{Fore.RED}[-] Wordlist not found!{Style.RESET_ALL}")
        return

    extension = input(f"{Fore.GREEN}Enter file extension (e.g., .php) or leave blank: {Style.RESET_ALL}").strip()
    print(f"{Fore.YELLOW}[+] Starting Directory Search...{Style.RESET_ALL}")
    
    q = Queue()
    for word in words:
        q.put(word)

    total_words = len(words)
    worker.completed = 0
    lock = threading.Lock()

    print(f"{Fore.YELLOW}[+] Total words to try: {total_words}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[+] Using {thread_count} threads{Style.RESET_ALL}\n")

    threads = []
    for _ in range(thread_count):
        t = threading.Thread(target=worker, args=(url, extension, q, total_words, lock))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print(f"\n{Fore.GREEN}[+] Directory Search Finished!{Style.RESET_ALL}")
