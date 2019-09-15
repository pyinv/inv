#!/usr/bin/env python3
"""Config for the example inventory."""

from inv import Inventory
from inv.asset_code import Damm32AssetCode

inventory = Inventory(
    asset_code_type=Damm32AssetCode,
)
