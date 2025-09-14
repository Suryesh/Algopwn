# Algohunt

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

2. Install dependencies (recommended to use a virtualenv):
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```
   Or install manually:
    ```bash
    pip install requests colorama
    ```

> `requirements.txt` should contain:
