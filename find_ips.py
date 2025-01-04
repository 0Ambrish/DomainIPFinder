import dns.resolver
import argparse
from urllib.parse import urlparse

# Cloudflare IP ranges (partial, for demonstration purposes)
CLOUDFLARE_IP_RANGES = [
    "104.16.0.0/12",
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
    Checks if an IP belongs to Cloudflare's public range.
    """
    from ipaddress import ip_address, ip_network
    return any(ip_address(ip) in ip_network(range) for range in CLOUDFLARE_IP_RANGES)

def resolve_domain(domain):
    """
    Resolves the IP address of a domain using dnspython.
    """
    try:
        answers = dns.resolver.resolve(domain, 'A')
        return [answer.to_text() for answer in answers]
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.Timeout):
        return []

def find_ips(input_file, ips_only=False):
    """
    Resolves IPs for domains/URLs in the input file and prints the results.
    """
    try:
        with open(input_file, "r") as infile:
            urls = infile.read().splitlines()
            for url in urls:
                domain = extract_domain(url)
                ips = resolve_domain(domain)
                if ips:
                    for ip in ips:
                        if is_cloudflare_ip(ip):
                            print(f"{domain}: {ip} (Cloudflare)" if not ips_only else f"{ip}")
                        else:
                            print(f"{domain}: {ip}" if not ips_only else f"{ip}")
                else:
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
