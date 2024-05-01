# Ciphercheck

This tool checks if a specific TLS ciphersuite is able to bypass a WAF.

I came across this blogpost: https://blog.pwn.al/waf/bypass/ssl/2018/07/02/web-application-firewall-bypass.html and I thought it could be interesting to automate this a little bit.

## Installation

- git clone https://github.com/stark0de/ciphercheck
- cd ciphercheck
- pip3 install -r requirements.txt

## Usage
```
options:
  -h, --help            show this help message and exit
  -u URL, --url URL     Target URL
  -c CIPHERSUITE_FILE, --ciphersuite-file CIPHERSUITE_FILE
                        Path to the file with the ciphersuite list
  -r {supported_ciphersuites,content_changes,both,all}, --results {supported_ciphersuites,content_changes,both,all}
                        Which results to show: supported_ciphersuites only shows when a ciphersuite is supported, content_changes shows when a certain ciphersuite receives a different result than the first request, both show the two
                        mentioned before, and all shows the ciphersuite errors as well
```

Example: python3 ciphercheck.py -u https://example.com -c cipherlist.txt -r all

## Notes
- This technique only makes sense with HTTPS-based websites.
- The cipherlist was obtained from https://curl.se/docs/ssl-ciphers.html
- The tls_max thing is tested in it's multiple possible values (1.0, 1.1, 1.2 and 1.3) because I noticed that curl just using --ciphers was offering more ciphers to the server instead of just the one I wanted it to offer, and this fixed it, apparently.
