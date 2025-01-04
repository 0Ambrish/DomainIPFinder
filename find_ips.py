import socket
import argparse
from urllib.parse import urlparse

def extract_domain(url):
    """
    Extracts the domain name from a URL or returns the input if it's already a domain.
    """
    parsed_url = urlparse(url)
    return parsed_url.netloc if parsed_url.netloc else url

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
                    if ips_only:
                        print(ip)
                    else:
                        print(f"{domain}: {ip}")
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
