# Algopwn

**Algopwn — Algolia API Key Analyzer & (authorized) Exploiter**

Algopwn helps security practitioners quickly assess Algolia API key exposures. The tool prompts for App ID and API key, fetches key metadata and ACLs, and classifies keys as informative (read-only) or sensitive (modifiable). For sensitive keys, Algopwn lists indexes, fetches index data and settings, and — only after interactive confirmation — can apply a reversible PoC update and print a copy-paste verification URL.

> ⚠️ **Important**: Only use Algopwn against applications you own or have explicit written permission to test (bug bounty scope, pentest engagement, etc.). Misuse may be illegal and unethical.

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


## Installation

1. Clone the repo:
    ```
    git clone https://github.com/Suryesh/Algopwn.git
    cd Algopwn
    ```

2. Install dependencies:
   ```
    pip install requests colorama
    ```

---

## Help
```
python3 algopwn.py -h
```

## Usage

1. Run the script `python3 algopwn.py` and follow the prompts:
2. Enter the Algolia App ID and API key when prompted.
3. The tool prints key info (JSON), then:
   - If the key is **informative only** (e.g., `search`, `listIndexes`, `settings`), the tool reports this and exits.
   - If the key is **sensitive** (e.g., `editSettings`, `addObject`, `deleteIndex`), the tool asks if you want to proceed with exploitation steps.
4. If you choose to proceed, you can pick an index, view its data/settings, and confirm an update. After updating, a PoC URL is printed.

```
python3 algopwn.py

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


If a sensitive key is detected:

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
