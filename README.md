# Ciphercheck

This tool checks if a specific TLS ciphersuite is able to bypass a WAF.

I came across this blogpost: https://blog.pwn.al/waf/bypass/ssl/2018/07/02/web-application-firewall-bypass.html and I thought it could be interesting to automate this a little bit.

The tool just checks if the results retrieved by curl vary from the results of the first request by using different ciphersuites. It makes sense to test this against sites returning generic 403 codes (but knowing somehow there is a WAF)  or "blocked-by-WAF" error pages.

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
- The curl version I used when I was writing the script is: curl 7.88.1 (x86_64-pc-linux-gnu) libcurl/7.88.1 OpenSSL/3.0.8 zlib/1.3 brotli/1.0.9 zstd/1.5.5 libidn2/2.3.3 libpsl/0.21.2 (+libidn2/2.3.3) libssh2/1.10.0 nghttp2/1.52.0 librtmp/2.3. Release-Date: 2023-02-20. Just in case someone needs to replicate the exact conditions.
