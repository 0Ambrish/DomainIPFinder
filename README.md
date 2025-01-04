DomainIPFINDER is a lightweight Python tool that resolves IP addresses for domains or URLs listed in a text file. It is easy to use and identifies Cloudflare-protected domains.

**Features**

Domain to IP Resolution: Resolves the IP for each domain or URL.
Cloudflare Detection: Identifies Cloudflare edge server IPs.
Flexible Output: Outputs both domain-IP pairs or only IP addresses.
Error Handling: Handles invalid or unreachable domains gracefully.

**COMMANDS**

git clone https://github.com/yourusername/DomainIPResolver.git

cd DomainIPResolver

**Run the Script:**

python3 find_ips.py -i domains.txt

python3 find_ips.py -i domains.txt --ips-only

**For Help**

python3 find_ips.py -h
