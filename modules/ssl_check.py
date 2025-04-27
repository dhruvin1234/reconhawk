import ssl
import socket
import OpenSSL

def ssl_check(domain):
    try:
        # Create a connection to the domain over HTTPS (port 443)
        conn = ssl.create_default_context().wrap_socket(
            socket.socket(socket.AF_INET), server_hostname=domain)
        conn.connect((domain, 443))
        
        # Get the SSL certificate
        cert = conn.getpeercert()
        
        # Print SSL certificate details in line-by-line format
        print(f"\n[+] SSL Certificate Information for {domain}:")
        
        # Extract and print issuer
        issuer = dict(x[0] for x in cert['issuer'])
        print(f"  Issuer: Country={issuer.get('countryName', 'N/A')}, "
              f"Organization={issuer.get('organizationName', 'N/A')}, "
              f"Common Name={issuer.get('commonName', 'N/A')}")
        
        # Extract and print subject
        subject = dict(x[0] for x in cert['subject'])
        print(f"  Subject: Common Name={subject.get('commonName', 'N/A')}")
        
        # Print validity dates
        print(f"  Valid From: {cert['notBefore']}")
        print(f"  Valid Until: {cert['notAfter']}")
        
        conn.close()
    
    except Exception as e:
        print(f"\033[91m[-] SSL Error: {str(e)}\033[0m")
