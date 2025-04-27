import requests
from colorama import Fore, Style
import threading

def grab_http_headers(url):
    try:
        response = requests.get(url, timeout=5)
        print(f"{Fore.GREEN}[+] {url} - HTTP Headers:{Style.RESET_ALL}")
        for header, value in response.headers.items():
            print(f"{Fore.RED}{header}: {value}{Style.RESET_ALL}")
    except requests.RequestException as e:
        print(f"{Fore.RED}[-] Error retrieving headers for {url}: {e}{Style.RESET_ALL}")

def header_grabber_main(urls_input, thread_count):
    urls = urls_input.split(',')
    threads = []
    
    for url in urls:
        thread = threading.Thread(target=grab_http_headers, args=(url.strip(),))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print(f"{Fore.GREEN}[+] HTTP Header Grabber Finished!{Style.RESET_ALL}")
