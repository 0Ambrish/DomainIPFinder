import socket
import argparse

def find_ips(input_file, output_file, ips_only=False):
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        domains = infile.read().splitlines()
        for domain in domains:
            try:
                ip = socket.gethostbyname(domain)
                if ips_only:
                    outfile.write(f"{ip}\n")
                else:
                    outfile.write(f"{domain}: {ip}\n")
                print(f"{domain}: {ip}" if not ips_only else ip)
            except socket.gaierror:
                if not ips_only:
                    outfile.write(f"{domain}: No IP found\n")
                    print(f"{domain}: No IP found")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find IPs for a list of domains.")
    parser.add_argument("-i", "--input", default="domains.txt", help="Input file with domain names (default: domains.txt)")
    parser.add_argument("-o", "--output", default="resolved_ips.txt", help="Output file for resolved IPs (default: resolved_ips.txt)")
    parser.add_argument("--ips-only", action="store_true", help="Output only IPs without domain names")
    
    args = parser.parse_args()
    
    print("Resolving domain IPs...")
    find_ips(args.input, args.output, args.ips_only)
    print(f"Results saved to {args.output}")
