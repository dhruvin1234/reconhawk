import sys
from colorama import Fore, Style
from modules import info_gathering
from modules import port_scanner
from modules import dir_search
from modules import domain_search
from modules import admin_finder  # Import the admin panel finder module
from modules import http_header_grabber 
from modules.xss_test import xss_test
from modules.sql_injection_test import sql_injection_test
from modules.ssl_check import ssl_check



def main():
    while True:
        print(f"{Fore.YELLOW}\n--- ReconHawk Menu ---{Style.RESET_ALL}")
        print(f"{Fore.CYAN}1. Information Gathering{Style.RESET_ALL}")
        print(f"{Fore.CYAN}2. Port Scanning{Style.RESET_ALL}")
        print(f"{Fore.CYAN}3. Directory Search{Style.RESET_ALL}")
        print(f"{Fore.CYAN}4. Domain Searching{Style.RESET_ALL}")
        print(f"{Fore.CYAN}5. Admin Panel Finder{Style.RESET_ALL}")  # New menu option for Admin Panel Finder
        
        # Added color for options 6 to 9
        print(f"{Fore.CYAN}6. HTTP Header Grabber{Style.RESET_ALL}")
        print(f"{Fore.CYAN}7. XSS Payload Testing{Style.RESET_ALL}")
        print(f"{Fore.CYAN}8. SQL Injection Testing{Style.RESET_ALL}")
        print(f"{Fore.CYAN}9. SSL/TLS Security Check{Style.RESET_ALL}")
        
        print(f"{Fore.CYAN}10. Exit{Style.RESET_ALL}")
        choice = input(f"{Fore.GREEN}Enter your choice: {Style.RESET_ALL}")

        if choice == '1':
            domain = input(f"{Fore.GREEN}Enter domain name: {Style.RESET_ALL}")
            ip = input(f"{Fore.GREEN}Enter IP for Shodan search (leave blank if not needed): {Style.RESET_ALL}")
            ip = ip.strip() if ip else None
            print(f"{Fore.YELLOW}[+] Starting Information Gathering...{Style.RESET_ALL}")
            info_gathering.run_info_gathering(domain, ip)

        elif choice == '2':
            target = input(f"{Fore.GREEN}Enter target IP or domain: {Style.RESET_ALL}")
            start_port = int(input(f"{Fore.GREEN}Enter start port: {Style.RESET_ALL}"))
            end_port = int(input(f"{Fore.GREEN}Enter end port: {Style.RESET_ALL}"))
            thread_no = int(input(f"{Fore.GREEN}Enter number of threads: {Style.RESET_ALL}"))
            port_scanner.scan_ports(target, start_port, end_port, thread_no)

        elif choice == '3':
            url = input(f"{Fore.GREEN}Enter target URL (e.g., https://example.com): {Style.RESET_ALL}")
            wordlist = input(f"{Fore.GREEN}Enter path to wordlist: {Style.RESET_ALL}")
            thread_count = int(input(f"{Fore.GREEN}Enter number of threads: {Style.RESET_ALL}"))
            dir_search.directory_search(url, wordlist, thread_count)

        elif choice == '4':
            domain = input(f"{Fore.GREEN}Enter domain name: {Style.RESET_ALL}")
            wordlist = input(f"{Fore.GREEN}Enter path to wordlist (leave blank to use default): {Style.RESET_ALL}")
            thread_count = int(input(f"{Fore.GREEN}Enter number of threads: {Style.RESET_ALL}"))
            domain_search.domain_search_main(domain, wordlist, thread_count)

        elif choice == '5':
            url = input(f"{Fore.GREEN}Enter target URL (e.g., https://example.com): {Style.RESET_ALL}")
            wordlist_input = input(f"{Fore.GREEN}Enter path to admin wordlist (leave blank to use default): {Style.RESET_ALL}")
            threads = int(input(f"{Fore.GREEN}Enter number of threads: {Style.RESET_ALL}"))
            admin_finder.admin_finder_main(url, wordlist_input or None, threads)  # Call the Admin Finder function
        elif choice == '6':
            urls_input = input(f"{Fore.GREEN}Enter URLs (comma separated): {Style.RESET_ALL}")
            threads = int(input(f"{Fore.GREEN}Enter number of threads: {Style.RESET_ALL}"))
            http_header_grabber.header_grabber_main(urls_input, threads)
        elif choice == "7":
            url = input(f"{Fore.GREEN}Enter the domain (e.g., example.com/?param=): {Style.RESET_ALL}")
            file_option = input(f"{Fore.GREEN}Do you want to use a custom payload file? (y/n): {Style.RESET_ALL}").strip().lower()
            if file_option == "y":
                file_path = input(f"{Fore.GREEN}Enter the payload file path: {Style.RESET_ALL}")
                xss_test(url, file_path)
            else:
                xss_test(url)
        elif choice == "8":
            url = input(f"{Fore.GREEN}Enter the domain (e.g., example.com/?param=): {Style.RESET_ALL}").strip()
            sql_injection_test(url)

        elif choice == '9':
            domain = input(f"{Fore.GREEN}Enter the domain (e.g., example.com): {Style.RESET_ALL}")
            ssl_check(domain)

        elif choice == '10':
            print(f"{Fore.RED}Exiting ReconHawk...{Style.RESET_ALL}")
            break

        else:
            print(f"{Fore.RED}Invalid choice. Try again.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
