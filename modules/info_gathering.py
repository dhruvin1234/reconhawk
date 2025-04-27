import socket
import whois
import dns.resolver
import requests
from colorama import Fore, Style

def run_info_gathering(domain):
    print(f"\n{Fore.YELLOW}[ WHOIS Information ]{Style.RESET_ALL}")
    try:
        py = whois.whois(domain)
        print(f"{Fore.RED}Domain Name:{Style.RESET_ALL} {py.domain_name}")
        print(f"{Fore.RED}Registrar:{Style.RESET_ALL} {py.registrar}")
        print(f"{Fore.RED}Creation Date:{Style.RESET_ALL} {py.creation_date}")
        print(f"{Fore.RED}Expiration Date:{Style.RESET_ALL} {py.expiration_date}")
        print(f"{Fore.RED}Registrant Country:{Style.RESET_ALL} {py.country}")
    except Exception as e:
        print(f"{Fore.RED}[-] WHOIS error:{Style.RESET_ALL} {e}")

    print(f"\n{Fore.YELLOW}[ DNS Information ]{Style.RESET_ALL}")
    try:
        for record_type in ['A', 'NS', 'MX', 'TXT']:
            answers = dns.resolver.resolve(domain, record_type)
            for rdata in answers:
                print(f"{Fore.RED}{record_type} Record:{Style.RESET_ALL} {rdata.to_text()}")
    except Exception as e:
        print(f"{Fore.RED}[-] DNS error:{Style.RESET_ALL} {e}")

    print(f"\n{Fore.YELLOW}[ Geolocation Information ]{Style.RESET_ALL}")
    try:
        ip_address = socket.gethostbyname(domain)
        response = requests.get(f"https://geolocation-db.com/json/{ip_address}").json()
        print(f"{Fore.RED}IP Address:{Style.RESET_ALL} {ip_address}")
        print(f"{Fore.RED}Country:{Style.RESET_ALL} {response['country_name']}")
        print(f"{Fore.RED}City:{Style.RESET_ALL} {response['city']}")
        print(f"{Fore.RED}State:{Style.RESET_ALL} {response['state']}")
        print(f"{Fore.RED}Latitude:{Style.RESET_ALL} {response['latitude']}")
        print(f"{Fore.RED}Longitude:{Style.RESET_ALL} {response['longitude']}")
    except Exception as e:
        print(f"{Fore.RED}[-] Geolocation error:{Style.RESET_ALL} {e}")
