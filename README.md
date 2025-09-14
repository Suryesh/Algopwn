# Algopwn

**Algohunt — Algolia API Key Analyzer & (authorized) Exploiter**

Algohunt helps security researchers and bug-bounty hunters quickly audit Algolia API keys, determine their ACLs, enumerate indexes, and — if explicitly authorized — perform a controlled PoC update (non-destructive by design except where explicitly requested by the user). After a successful update the tool prints a PoC verification URL you can open in a browser.

> ⚠️ **Important**: Only use Algohunt against applications you own or have explicit written permission to test (bug bounty scope, pentest engagement, etc.). Misuse may be illegal and unethical.

---

## Features

- Prompt-based interactive workflow (no required CLI args).
- Fetches key metadata and ACLs from Algolia.
- Distinguishes **informative (read-only)** ACLs vs **sensitive (modify/delete)** ACLs.
- If sensitive ACLs are present, lists indexes and allows you to:
  - fetch index data (single index),
  - fetch index settings,
  - optionally update `highlightPreTag` to a PoC value (e.g., `"hacked"`).
- Prints a copy-paste **PoC verification URL** after a successful update.
- Colorised terminal output for readability.
- Small, dependency-light: uses `requests` and `colorama`.

---

## Suggested repository name

`Algohunt` (recommended) — short and memorable.

---

## Quick demo (what to expect)

1. Run the script:
    ```bash
    python3 algohunt.py
    ```
2. Enter the Algolia App ID and API key when prompted.
3. The tool prints key info (JSON), then:
   - If the key is **informative only** (e.g., `search`, `listIndexes`, `settings`), the tool reports this and exits.
   - If the key is **sensitive** (e.g., `editSettings`, `addObject`, `deleteIndex`), the tool asks if you want to proceed with exploitation steps.
4. If you choose to proceed, you can pick an index, view its data/settings, and confirm an update. After updating, a PoC URL is printed:
    ```
    https://{appID}-dsn.algolia.net/1/indexes/{index_name}/settings?x-algolia-application-id={appID}&x-algolia-api-key={apiKey}
    ```

---

## Installation

1. Clone the repo:
    ```bash
    git clone https://github.com/<your-username>/Algohunt.git
    cd Algohunt
    ```

2. Install dependencies:
   ```
    pip install requests colorama
    ```

---

## Help
```
python3 algohunt.py -h
```

## Usage

Run the script and follow the prompts:

```
python3 algohunt.py
```
```
   _   _               ___
  /_\ | | __ _  ___   / _ \__      ___ __
 //_\\| |/ _` |/ _ \ / /_)/\ \ /\ / / '_ \
/  _  \ | (_| | (_) / ___/  \ V  V /| | | |
\_/ \_/_|\__, |\___/\/       \_/\_/ |_| |_|
         |___/

      Algolia API Key Exploiter by Suryesh

You can follow me on Twitter/X: https://x.com/Suryesh_92

Subscribe to my Youtube Channel: https://www.youtube.com/@HackWithSuryesh

Enter Algolia Application ID: MH9A52MZTO
Enter Algolia API Key: 4d89644522b528406ec821a713da60fe

{ "info": { ... } }

This key only has ['search'] permissions. So, it is Informative only.


### If a sensitive key is detected:

This key has sensitive ACLs: ['editSettings', 'deleteObject', etc.]
Do you want to proceed with exploitation? (y/n): y

Indexes available:
1. products_v1
2. users_public

Enter the index name to work with: products_v1
[fetch data]
[fetch settings]
Do you want to update this index's settings with payload (highlightPreTag=hacked)? (y/n): y
[+] Update Response: {...}
[+] PoC Verification URL:
https://MH9A52MZTO-dsn.algolia.net/1/indexes/products_v1/settings?x-algolia-application-id=MH9A52MZTO&x-algolia-api-key=4d896...

```
