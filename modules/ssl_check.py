import ssl
import socket
from colorama import Fore, Style

def ssl_check(domain):
    try:
        conn = ssl.create_default_context().wrap_socket(
            socket.socket(socket.AF_INET), server_hostname=domain)
        conn.connect((domain, 443))
        
        cert = conn.getpeercert()
        
        print(f"\n{Fore.YELLOW}[+] SSL Certificate Information for {domain}:{Style.RESET_ALL}\n")
        
        # Extract and print issuer
        issuer = dict(x[0] for x in cert['issuer'])
        print(f"{Fore.CYAN}Issuer Information:{Style.RESET_ALL}")
        print(f"  {Fore.RED}Country:{Style.RESET_ALL} {issuer.get('countryName', 'N/A')}")
        print(f"  {Fore.RED}Organization:{Style.RESET_ALL} {issuer.get('organizationName', 'N/A')}")
        print(f"  {Fore.RED}Common Name:{Style.RESET_ALL} {issuer.get('commonName', 'N/A')}\n")
        
        # Extract and print subject
        subject = dict(x[0] for x in cert['subject'])
        print(f"{Fore.CYAN}Subject Information:{Style.RESET_ALL}")
        print(f"  {Fore.RED}Common Name:{Style.RESET_ALL} {subject.get('commonName', 'N/A')}\n")
        
        # Print validity dates
        print(f"{Fore.CYAN}Certificate Validity:{Style.RESET_ALL}")
        print(f"  {Fore.RED}Valid From:{Style.RESET_ALL} {cert['notBefore']}")
        print(f"  {Fore.RED}Valid Until:{Style.RESET_ALL} {cert['notAfter']}\n")
        
        print(f"{Fore.YELLOW}" + "-" * 40 + f"{Style.RESET_ALL}")
        
        conn.close()
    
    except Exception as e:
        print(f"{Fore.RED}[-] SSL Error: {str(e)}{Style.RESET_ALL}")
