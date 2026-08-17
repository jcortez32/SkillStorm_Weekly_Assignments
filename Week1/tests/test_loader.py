import pytest
from support_api.models import RestockItem
from support_api.store import load_manifest
from support_api.store import restock_manifestNotFoundError
from pydantic import ValidationError
from support_api.sample_data import SAMPLE_MANIFEST

from pathlib import Path


def test_missing_file():
   with pytest.raises(restock_manifestNotFoundError):
       load_manifest(None)

#SAMPLE_MANIFEST[0] is a valid row 
def test_valid_row():
     valid_restock_manifest, invalid_restock_manifest = load_manifest(Path("data/restock_manifest.json"))
     print(valid_restock_manifest[0])
     assert valid_restock_manifest[0] == RestockItem(sku='SKU-1001', warehouse='west-1', quantity=25, unit_cost=12.5, category='electronics')

#SAMPLE_MANIFEST[0] is a valid row 
def test_invalid_row():
    valid_restock_manifest, invalid_restock_manifest = load_manifest(Path("data/restock_manifest.json"))
    assert len(invalid_restock_manifest) >= 0

#Check that there are 8 valid rows and 4 invalid rows
def test_num_valid_and_invalid():
    valid_restock_manifest, invalid_restock_manifest = load_manifest(Path("data/restock_manifest.json"))
    assert len(valid_restock_manifest) == 8 and len(invalid_restock_manifest) == 4

#SAMPLE_MANIFEST[8] should raise category error 
#SAMPLE_MANIFEST[9] should raise quantity error
#SAMPLE_MANIFEST[10] should raise a unit cost error
@pytest.mark.parametrize("invalid_field_data", [SAMPLE_MANIFEST[8],SAMPLE_MANIFEST[9],SAMPLE_MANIFEST[10]])
def test_are_fields_valid(invalid_field_data):
    pytest.raises(ValidationError)
