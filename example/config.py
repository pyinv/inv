#!/usr/bin/env python3
"""Config for the example inventory."""

from pathlib import Path

from inv import Inventory
from inv.asset_code import Damm32AssetCode

inventory = Inventory(
    Path(__file__).parent,
    asset_code_type=Damm32AssetCode,
    org="ABC",
)
