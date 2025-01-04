import socket
import argparse
import os
from urllib.parse import urlparse

def extract_domain(url):
    """
    Extracts the domain name from a URL or returns the input if it's already a domain.
    """
    parsed_url = urlparse(url)
    return parsed_url.netloc if parsed_url.netloc else url

def find_ips(input_file, output_with_domains, output_ips_only):
    """
    Resolves IPs for domains/URLs in the input file and saves the results.
    """
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' does not exist.")
        return

    with open(input_file, "r") as infile, \
         open(output_with_domains, "w") as outfile_with_domains, \
         open(output_ips_only, "w") as outfile_ips_only:
        urls = infile.read().splitlines()
        for url in urls:
            domain = extract_domain(url)
            try:
                ip = socket.gethostbyname(domain)
                outfile_with_domains.write(f"{domain}: {ip}\n")
                outfile_ips_only.write(f"{ip}\n")
                print(f"{domain}: {ip}")
            except socket.gaierror:
                outfile_with_domains.write(f"{domain}: No IP found\n")
                print(f"{domain}: No IP found")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find IPs for a list of domains or URLs.")
    parser.add_argument("-i", "--input", default="domains.txt", help="Input file with domain names or URLs (default: domains.txt)")
    parser.add_argument("--with-domains", default="resolved_ips_with_domains.txt", help="Output file with domains and their IPs (default: resolved_ips_with_domains.txt)")
    parser.add_argument("--ips-only", default="resolved_ips_only.txt", help="Output file with only IPs (default: resolved_ips_only.txt)")
    
    args = parser.parse_args()
    
    print("Resolving domain IPs...")
    find_ips(args.input, args.with_domains, args.ips_only)
    print(f"Results saved to:\n  - {args.with_domains}\n  - {args.ips_only}")
