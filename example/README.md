# Example of Inventory

This folder contains an example inventory.

## Format

- `meta`
    - Details of manufacturers and models
    - `manufacturer/model.yml`
    - `model.yml`
        - Manufacturer is N/A
- `config.py`
    - Python file that configures the inventory.
- `ABC-XYZ-XYZ_foobar`
    - A location or container
    - Only the asset code matters. Anything after the first `_` is arbitrary.
    - Contains `data.yml` which describes the container.