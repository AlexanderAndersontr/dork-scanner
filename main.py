import requests
import argparse
import json
import sys
import random
import urllib3
from datetime import datetime

urllib3.disable_warnings()

def banner():
    print(r"""
 █████╗ ██╗     ███████╗██╗  ██╗
██╔══██╗██║     ██╔════╝╚██╗██╔╝
███████║██║     █████╗   ╚███╔╝ 
██╔══██║██║     ██╔══╝   ██╔██╗ 
██║  ██║███████╗███████╗██╔╝ ██╗
╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝
        DORK SCANNER
    """)
    print(f"Başlangıç: {datetime.now()}\n")

parse = argparse.ArgumentParser(description="Dork Tarayıcı")
parse.add_argument("-f", required=True)
parse.add_argument("-o", action='store_true')
args = parse.parse_args()

banner()

url = "https://google.serper.dev/search"

dorkslist = []
proxies_list = []
api = ""

# proxy yükle
try:
    with open("proxy.txt", "r") as file:
        proxies_list = file.read().splitlines()
except:
    print("Proxy dosyası yok!")
    sys.exit()

# API yükle
try:
    with open("api.txt", "r") as file:
        api = file.read().strip()
except:
    print("API yok!")
    sys.exit()

headers = {
    "X-API-KEY": api,
    "Content-Type": "application/json"
}

# dork yükle
with open(args.f, "r") as file:
    dorkslist = file.read().splitlines()

print(f"[+] {len(dorkslist)} dork yüklendi\n")

for dork in dorkslist:
    print(f"[~] Aranıyor: {dork}")

    payload = {"q": dork}

    proxy = random.choice(proxies_list)

    proxies = {
        "http": f"http://{proxy}",
        "http": f"http://{proxy}"
    }

    try:
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            proxies=proxies,
            timeout=5,
            verify=False
        )

        if response.status_code == 200:
            data = response.json()
            results = data.get("organic", [])

            if not results:
                print("[-] Sonuç yok\n")
                continue

            for r in results:
                link = r.get("link")
                if link:
                    print(f"[+] {link}")

                    if args.o:
                        with open("results.txt", "a", encoding="utf-8") as f:
                            f.write(f"{dork} | {link}\n")

            print()

        else:
            print(f"[!] API Hatası: {response.status_code}\n")

    except Exception as e:
        print(f"[!] Hata: {e}\n")

print("[✓] Bitti")