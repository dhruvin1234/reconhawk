import socket
import whois
import dns.resolver
from colorama import Fore, Style
import threading

def find_ip(domain):
    try:
        ip = socket.gethostbyname(domain)
        print(f"{Fore.GREEN}[+] IP Address: {ip}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[-] Failed to get IP: {e}{Style.RESET_ALL}")

def whois_lookup(domain):
    try:
        w = whois.whois(domain)
        print(f"{Fore.GREEN}[+] WHOIS Info:{Style.RESET_ALL}")
        print(w)
    except Exception as e:
        print(f"{Fore.RED}[-] WHOIS lookup failed: {e}{Style.RESET_ALL}")

def dns_records(domain):
    try:
        print(f"{Fore.GREEN}[+] DNS Records:{Style.RESET_ALL}")
        for record_type in ['A', 'MX', 'NS']:
            try:
                answers = dns.resolver.resolve(domain, record_type)
                for answer in answers:
                    print(f"{record_type}: {answer.to_text()}")
            except Exception:
                pass
    except Exception as e:
        print(f"{Fore.RED}[-] DNS lookup failed: {e}{Style.RESET_ALL}")

def subdomain_enum(domain, wordlist_path, thread_count):
    try:
        with open(wordlist_path, 'r') as f:
            subdomains = f.read().splitlines()
    except FileNotFoundError:
        print(f"{Fore.RED}[-] Wordlist not found!{Style.RESET_ALL}")
        return

    total_subdomains = len(subdomains)
    found_subdomains = []
    processed_count = 0
    lock = threading.Lock()

    def worker(sublist):
        nonlocal processed_count
        for sub in sublist:
            url = f"{sub}.{domain}"
            try:
                socket.gethostbyname(url)
                with lock:
                    print(f"{Fore.RED}[+] Found Subdomain: {url}{Style.RESET_ALL}")
                    found_subdomains.append(url)
            except:
                pass
            finally:
                with lock:
                    processed_count += 1
                    print(f"{Fore.MAGENTA}[*] Processed: {processed_count}/{total_subdomains}{Style.RESET_ALL}", end='\r')

    chunk_size = len(subdomains) // thread_count
    threads = []

    for i in range(thread_count):
        chunk = subdomains[i*chunk_size : (i+1)*chunk_size]
        t = threading.Thread(target=worker, args=(chunk,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"\n{Fore.YELLOW}[+] Subdomain enumeration complete! Found {len(found_subdomains)} subdomains.{Style.RESET_ALL}")

def domain_search_main(domain, wordlist_path, thread_count):
    find_ip(domain)
    whois_lookup(domain)
    dns_records(domain)
    subdomain_enum(domain, wordlist_path, thread_count)


# /usr/share/wordlists/amass/subdomains-top1mil-5000.txt