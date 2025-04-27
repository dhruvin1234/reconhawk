import socket
import whois
import dns.resolver
import shodan
import requests

def run_info_gathering(domain, ip=None):
    print("[+] Getting WHOIS info...")
    try:
        py = whois.whois(domain)
        print("WHOIS info found.")
        print("Name: {}".format(py.domain_name))
        print("Registrar: {}".format(py.registrar))
        print("Creation Date: {}".format(py.creation_date))
        print("Expiration Date: {}".format(py.expiration_date))
        print("Registrant Country: {}".format(py.country))
    except Exception as e:
        print(f"[-] WHOIS error: {e}")

    print("[+] Getting DNS info...")
    try:
        for record_type in ['A', 'NS', 'MX', 'TXT']:
            answers = dns.resolver.resolve(domain, record_type)
            for rdata in answers:
                print(f"[+] {record_type} Record: {rdata.to_text()}")
    except Exception as e:
        print(f"[-] DNS error: {e}")

    print("[+] Getting geolocation info...")
    try:
        ip_address = socket.gethostbyname(domain)
        response = requests.get(f"https://geolocation-db.com/json/{ip_address}").json()
        print("[+] Country: {}".format(response['country_name']))
        print("[+] Latitude: {}".format(response['latitude']))
        print("[+] Longitude: {}".format(response['longitude']))
        print("[+] City: {}".format(response['city']))
        print("[+] State: {}".format(response['state']))
    except Exception as e:
        print(f"[-] Geolocation error: {e}")

    if ip:
        print("[+] Getting Shodan info...")
        try:
            api = shodan.Shodan("aUVYZFTo6vKPjpSZFyPP9ZXVRuacxUi9")  # ⚡ Note: Hide your API key later!
            host = api.host(ip)
            print(f"[+] IP: {host['ip_str']}")
            print(f"[+] Organization: {host.get('org', 'n/a')}")
            print(f"[+] Operating System: {host.get('os', 'n/a')}")
            for item in host['data']:
                print(f"[+] Port: {item['port']}")
                print(f"[+] Banner: {item['data']}")
                print("-" * 20)
        except Exception as e:
            print(f"[-] Shodan error: {e}")

