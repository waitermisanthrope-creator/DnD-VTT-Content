#!/usr/bin/env python3
"""Offline validation for the immutable fantasy merchants workshop pack."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "packages/dnd.market.fantasy-merchants-1.0.0.json"
CATALOG = ROOT / "catalog/v3/index.json"
CATEGORIES = {"weapons", "armor", "materials", "consumables", "junk"}


def main():
    raw = PATH.read_bytes()
    data = json.loads(raw)
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    entries = [e for e in catalog["packages"] if e.get("id") == data["id"]]
    assert len(entries) == 1, "catalog entry missing or duplicated"
    entry = entries[0]
    assert entry["type"] == data["type"] == "craft"
    assert data["mode"] == "alchemy-ingredients"
    assert data["ingredients"] == [] and data["items"] == [], "compatibility envelope must be inert"
    market = data["merchantMarket"]
    assert market["schemaVersion"] == 1 and market["type"] == "market"
    assert market["id"] == data["id"] and market["version"] == data["version"]
    assert data["version"] == entry["version"] == "1.0.0"
    assert entry["bytes"] == len(raw), "byte count mismatch"
    assert entry["sha256"] == hashlib.sha256(raw).hexdigest(), "SHA-256 mismatch"
    assert entry["url"].endswith("/packages/" + PATH.name)
    traders = market["traders"]
    departments = market["departments"]
    assert len(traders) == 45 and len(departments) == 12
    ids = [trader["id"] for trader in traders]
    assert len(ids) == len(set(ids)), "duplicated vendor"
    assert len({d["id"] for d in departments}) == 12
    for t in traders:
        assert set(t["itemCategories"]).issubset(CATEGORIES)
        assert 0 <= t["deriveLimit"] <= 64
        assert len(t.get("nameContains", [])) <= 32
        assert t["template"] and t["name"]
        assert "stock" not in t, "items must be referenced, not copied"
    seen = set()
    for d in departments:
        assert d["name"] and d["traders"]
        for name in d["traders"]:
            assert name in ids, f"department {d['id']} references missing trader {name}"
            seen.add(name)
    assert seen == set(ids), "some vendors are invisible in the tree"
    assert {"exotic_weapon_dealer", "healer", "tailor"}.issubset(seen)
    assert entry["minClientVersionCode"] >= 10050
    print(f"FANTASY_MERCHANTS_PASS: {len(traders)} traders, {len(departments)} departments, SHA-256 verified")


if __name__ == "__main__":
    main()
