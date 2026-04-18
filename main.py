import requests
import argparse
import json

parse = argparse.ArgumentParser(description="THT Dork Scanner")
parse.add_argument("-f", help="Dorks Files", required=True)
parse.add_argument("-o", help="Output", required=False, action='store_true')

args = parse.parse_args()

url = "https://google.serper.dev/search"
dorkslist = []
api = ""

with open("api.txt", "r") as file:
    api = file.read().strip()

headers = {
    "X-API-KEY": api,
    "Content-Type": "application/json"
}

with open(args.f, "r") as file:
    dorkslist.extend(file.read().splitlines())
    print(f"Loaded {len(dorkslist)} dorks:")
    print(dorkslist)

for dork in dorkslist:
    dorks = {
        "q": dork
    }
    print(f"\nSearching for: {dork}")
    
    try:
        response = requests.post(url, json=dorks, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            
            for result in data.get("organic", []):
                link = result.get("link")
                if link:
                    print(f"Found link: {link}")
                    
                    if args.o:
                        with open("results.txt", "a", encoding="utf-8") as outfile:
                            outfile.write(f"{dork} | {link}\n")
        else:
            print(f"Error: API returned status code {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")

print("\nScan completed!")