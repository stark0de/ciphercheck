import requests
import subprocess
import sys
import argparse
import signal
from colorama import Fore, init
init()

def showbanner():
    bannertext='''
  ____ _       _                   _               _
 / ___(_)_ __ | |__   ___ _ __ ___| |__   ___  ___| | __
| |   | | '_ \| '_ \ / _ \ '__/ __| '_ \ / _ \/ __| |/ /
| |___| | |_) | | | |  __/ | | (__| | | |  __/ (__|   <
 \____|_| .__/|_| |_|\___|_|  \___|_| |_|\___|\___|_|\_|
        |_|

        --------------written by @stark0de1------------\n'''
    print(Fore.GREEN+bannertext+Fore.WHITE)

def handler(signum, frame):
    print(Fore.RED+"[-] Bye bye ;)"+Fore.WHITE)
    sys.exit()

signal.signal(signal.SIGINT, handler)

showbanner()

parser = argparse.ArgumentParser(description='Script to check if the WAF forwards requests to the webserver if it doesn\'t support a certain SSL/TLS ciphersuite')
parser.add_argument('-u', '--url', type=str, help='Target URL', required=True)
parser.add_argument('-c', '--ciphersuite-file', type=str, help='Path to the file with the ciphersuite list', required=True)
parser.add_argument('-r', '--results',help='Which results to show: supported_ciphersuites only shows when a ciphersuite is supported, content_changes shows when a certain ciphersuite receives a different result than the first request, both show the two mentioned before, and all shows the ciphersuite errors as well', required=True, choices=['supported_ciphersuites','content_changes', 'both', 'all'])

args = parser.parse_args()
url = args.url
initial = subprocess.Popen("curl --no-progress-meter "+url, stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)
initial_content = initial.communicate()[0].decode('utf-8')
cipher_suites=open(args.ciphersuite_file,"r")
results=args.results
positive_change=0
positive_cipher=0
tlsmax= ["1.0", "1.1", "1.2", "1.3"]

for cipher in cipher_suites:
    for tlsmaxvalue in tlsmax:
        try:
        # Specify cipher suite for the request
            p = subprocess.Popen("curl --no-progress-meter --tls-max "+tlsmaxvalue+" --ciphers "+cipher.strip()+" "+url, stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)
            stdout = p.communicate()[0].decode('utf-8')
            stderr = p.communicate()[1].decode('utf-8')
            if "SSL_ERROR_ZERO_RETURN" in stderr or "handshake failure" in stderr or "SSL_ERROR_SSL" in stderr or "no ciphers available" in stderr:
               if results == "all":
                  print(Fore.RED+"[-]"+Fore.WHITE+" Ciphersuite "+cipher.strip()+" not suitable for "+url+ "and tls max "+tlsmaxvalue)
        # Check if content is different from initial request
            elif len(stdout) > 0:
               if results == "supported_ciphersuites" or results == "both" or results == "all":
                  print(Fore.GREEN+"[+]"+Fore.WHITE+" Ciphersuite "+cipher.strip()+ " suitable for "+url+ "and tls max "+tlsmaxvalue)
               positive_cipher+=1
               if stdout != initial_content:
                   if results == "content_changes" or results == "both" or results == "all":
                      print(Fore.GREEN+"[+]"+Fore.WHITE+" Content differs using cipher suite: "+cipher.strip() +" and tls max "+tlsmaxvalue)
                   positive_change+=1
        except Exception as e:
            print(e)
if positive_cipher == positive_change:
    print(Fore.RED+"[-]"+Fore.WHITE+" All the supported ciphersuites show changes in relation to the first request. This is probably because the page's content is dynamic somehow, for instance, with an anti-CSRF token. Please check manually")
elif positive_change > 5:
    print(Fore.RED+"[-]"+Fore.WHITE+" The number of ciphersuites for which the content of the website changes is very high ("+ str(positive)+") in this case. This is probably because the page's content is dynamic somehow, for instance, with an anti-CSRF token. Please check manually")
