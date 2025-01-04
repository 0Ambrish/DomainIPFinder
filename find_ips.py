import socket
import argparse
from urllib.parse import urlparse
from ipaddress import ip_address, ip_network

# Known Cloudflare IP ranges
CLOUDFLARE_IP_RANGES = [
    "173.245.48.0/20",
    "103.21.244.0/22",
    "103.22.200.0/22",
    "103.31.4.0/22",
    "141.101.64.0/18",
    "108.162.192.0/18",
    "190.93.240.0/20",
    "188.114.96.0/20",
    "197.234.240.0/22",
    "198.41.128.0/17",
    "162.158.0.0/15",
    "104.16.0.0/13",
    "104.24.0.0/14",
    "172.64.0.0/13",
    "131.0.72.0/22",
]

def extract_domain(url):
    """
    Extracts the domain name from a URL or returns the input if it's already a domain.
    """
    parsed_url = urlparse(url)
    return parsed_url.netloc if parsed_url.netloc else url

def is_cloudflare_ip(ip):
    """
    Checks if the given IP is within known Cloudflare IP ranges.
    """
    ip_obj = ip_address(ip)
    for cidr in CLOUDFLARE_IP_RANGES:
        if ip_obj in ip_network(cidr):
            return True
    return False

def find_ips(input_file, ips_only=False):
    """
    Resolves IPs for domains/URLs in the input file and prints the results.
    """
    try:
        with open(input_file, "r") as infile:
            urls = infile.read().splitlines()
            for url in urls:
                domain = extract_domain(url)
                try:
                    ip = socket.gethostbyname(domain)
                    cloudflare_status = " (Cloudflare IP)" if is_cloudflare_ip(ip) else ""
                    if ips_only:
                        print(ip)
                    else:
                        print(f"{domain}: {ip}{cloudflare_status}")
                except socket.gaierror:
                    if not ips_only:
                        print(f"{domain}: No IP found")
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' does not exist.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find IPs for a list of domains or URLs.")
    parser.add_argument("-i", "--input", required=True, help="Input file with domain names or URLs")
    parser.add_argument("--ips-only", action="store_true", help="Output only IPs without domain names")
    
    args = parser.parse_args()
    
    print("Resolving domain IPs...")
    find_ips(args.input, args.ips_only)
