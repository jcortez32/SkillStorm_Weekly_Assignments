import json 
from pathlib import Path
from pydantic import ValidationError
from support_api.models import RestockItem

class restock_manifestStoreError(Exception):
    "general exception"

class restock_manifest_PATH_NonExistant(restock_manifestStoreError):
    "manifest file does not exist"

class invalidDataFormat(restock_manifestStoreError):
    "manifest data could not be loaded in due to format issues"

def load_manifest(path: Path | None = None) -> tuple[list[RestockItem], list[dict]]:
    print(f"\n--- FUNCTION NAME: {load_manifest.__name__} ---")

    resolved_path = path
    if path == None:
        resolved_path = Path("data/restock_manifest.json")
    try:
        raw_text = resolved_path.read_text(encoding="utf-8")
    except FileNotFoundError as e:
        raise restock_manifest_PATH_NonExistant(f"No manifest fixture at {resolved_path}") from e

    try:
        rows = json.loads(raw_text)
    except json.JSONDecodeError as e:
        raise invalidDataFormat(f"Manifest data could not be loaded in from {resolved_path}")

    valid_restock_manifest:list[RestockItem] = []
    invalid_restock_manifest:list[dict] = []

    for row in rows:
        try:
            valid_restock_manifest.append(RestockItem.model_validate(row))
        except ValidationError as e:
            error_message = [f"{e["loc"]} : {e["msg"]}" for e in e.errors()]
            invalid_restock_manifest.append({"id":row.get("id", "<no id>"), "errors":error_message})

    return valid_restock_manifest, invalid_restock_manifest

