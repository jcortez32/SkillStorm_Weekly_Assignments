from support_api.store import load_manifest
from pathlib import Path
valid_restock_manifest, invalid_restock_manifest = load_manifest(Path("data/restock_manifest.json"))
print("--- Valid Restock_Manifest ---")
print(valid_restock_manifest)
print(f"number of valid tickets is {len(valid_restock_manifest)}")


print("\n--- Invalid Restock_Manifest ---")
print(invalid_restock_manifest)
print(f"number of valid tickets is {len(invalid_restock_manifest)}")

