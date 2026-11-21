#!/usr/bin/env python3
"""Sync verified license status from WindFonts Vault catalog export into licenses/*/license-info.json.

Safety guarantees:
- Fetches https://api.windfonts.com/api/catalog/export?view=fonts directly (no proxy).
- Resolves directory -> canonical normalized key via data/dir-aliases.json (fallback: normalizedName / dir lower).
- ONLY upgrades entries where local verified is False/None AND vault licenseVerified is strictly True.
- Records verifiedSource = "vault" (and sets verifiedAt if currently null).
- Safely fills spdx from vault licenseSpdx when currently empty/null, and licenseName from vault licenseName
  when currently empty/null (never overwrites non-empty human-curated notes, license text files, or existing values).
"""

import argparse
import datetime
import json
import os
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_API_URL = "https://api.windfonts.com/api/catalog/export?view=fonts"
ALIASES_PATH = os.path.join(ROOT, "data", "dir-aliases.json")
LICENSES_DIR = os.path.join(ROOT, "licenses")
# Per AGENTS.md §2 6a: licenseName must be a real protocol name, never a tier slogan.
FORBIDDEN_LICENSE_NAMES = {
    "免费商用",
    "免费可商用",
    "开源商用",
    "个人免费",
    "个人用途",
    "试用版",
    "付费授权",
    "联系授权",
    "待核实",
}


def fetch_vault_catalog(url: str, timeout: int = 30) -> dict:
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    req = urllib.request.Request(url, headers={"User-Agent": "font-licenses/sync-verified-from-vault"})
    with opener.open(req, timeout=timeout) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    items = None
    if isinstance(payload, dict):
        if isinstance(payload.get("data"), list):
            items = payload["data"]
        elif isinstance(payload.get("fonts"), list):
            items = payload["fonts"]
    elif isinstance(payload, list):
        items = payload
    if items is None:
        raise RuntimeError("Unexpected vault catalog export payload shape")
    by_norm = {}
    for item in items:
        if not isinstance(item, dict):
            continue
        norm = (item.get("normalized") or "").strip().lower()
        if norm:
            by_norm[norm] = item
    return by_norm


def load_aliases(path: str) -> dict:
    if not os.path.isfile(path):
        return {}
    with open(path, "r", encoding="utf-8") as fh:
        raw = json.load(fh)
    dirs = raw.get("dirs") if isinstance(raw, dict) else {}
    return dirs if isinstance(dirs, dict) else {}


def resolve_canonical(dir_name: str, info: dict, aliases: dict) -> str:
    alias = aliases.get(dir_name)
    if isinstance(alias, dict) and alias.get("canonical"):
        return str(alias["canonical"]).strip().lower()
    if isinstance(alias, str) and alias.strip():
        return alias.strip().lower()
    norm = info.get("normalizedName") or info.get("norm") or dir_name
    return str(norm).strip().lower()


def main() -> int:
    parser = argparse.ArgumentParser(description="Backfill licenseVerified=true from Vault catalog export.")
    parser.add_argument("--url", default=DEFAULT_API_URL, help=f"Vault catalog export URL (default: {DEFAULT_API_URL})")
    parser.add_argument("--apply", action="store_true", help="Write changes to licenses/*/license-info.json (default: dry-run)")
    parser.add_argument("--today", default=datetime.date.today().isoformat(), help="Date string for verifiedAt when missing")
    args = parser.parse_args()

    vault = fetch_vault_catalog(args.url)
    aliases = load_aliases(ALIASES_PATH)

    stats = {
        "vault_total": len(vault),
        "vault_verified": sum(1 for v in vault.values() if v.get("licenseVerified") is True),
        "scanned": 0,
        "matched_vault_verified": 0,
        "already_verified": 0,
        "upgraded": 0,
        "spdx_filled": 0,
        "license_name_filled": 0,
    }
    changed_dirs = []

    for dir_name in sorted(os.listdir(LICENSES_DIR)):
        info_path = os.path.join(LICENSES_DIR, dir_name, "license-info.json")
        if not os.path.isfile(info_path):
            continue
        stats["scanned"] += 1
        with open(info_path, "r", encoding="utf-8") as fh:
            info = json.load(fh)

        canonical = resolve_canonical(dir_name, info, aliases)
        vf = vault.get(canonical)
        if not vf or vf.get("licenseVerified") is not True:
            continue

        stats["matched_vault_verified"] += 1
        if info.get("verified") is True:
            stats["already_verified"] += 1
            continue

        # Only upgrade verified: false/null -> true when vault explicitly has licenseVerified === true
        info["verified"] = True
        info["verifiedSource"] = "vault"
        if not info.get("verifiedAt"):
            info["verifiedAt"] = args.today
        if not info.get("verifiedBy"):
            info["verifiedBy"] = "vault"

        v_spdx = (vf.get("licenseSpdx") or "").strip()
        if v_spdx and not info.get("spdx"):
            info["spdx"] = v_spdx
            stats["spdx_filled"] += 1

        v_lname = (vf.get("licenseName") or "").strip()
        if v_lname and v_lname not in FORBIDDEN_LICENSE_NAMES and not info.get("licenseName"):
            info["licenseName"] = v_lname
            stats["license_name_filled"] += 1

        stats["upgraded"] += 1
        changed_dirs.append((dir_name, canonical, info.get("spdx"), info.get("licenseName")))

        if args.apply:
            with open(info_path, "w", encoding="utf-8") as fh:
                json.dump(info, fh, ensure_ascii=False, indent=2)
                fh.write("\n")

    mode = "APPLY" if args.apply else "DRY-RUN"
    print(f"[{mode}] {json.dumps(stats, ensure_ascii=False)}")
    for row in changed_dirs:
        print(f"  + {row[0]} ({row[1]}): spdx={row[2]!r} licenseName={row[3]!r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
