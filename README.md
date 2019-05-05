# PyInv

## Requirements

Python 3.6+

## What is PyInv?

For some time, SRO have been searching for a better inventory system to replace the current one. We found that whilst a Google Sheet is a reasonable solution, it has a lock on search and filtering, such that only one user can use it at a time. Additionally it offers a poor UX and is not particularly easy to use.

Our sister organisation, Student Robotics, uses a Git based Inventory system that whilst good at first, has become somewhat neglected. It is out of date, complex to use and contains numerous mistakes, both semantic and in file structure.

PyInv is a modular inventory and asset management system. It will support a number of storage formats, and various different front-ends (e.g GUI, CLI, Kiosk). It aims to be backwards compatible with the SR inventory, but **not** backwards compatible with the SRO inventory.

## What features will PyInv have?

- Tracking of asset locations, conditions and values
- Extensive audit tooling, state is re-creatable at any time.
- Customisable Inventory Schema and Attributes
- Prevention of Cross-organisation Code Conflicts
- Label generation and printing
- Modular Storage Backends, including conversion between formats
    - Git
    - SQL
- Modular Frontends
    - CLI
    - GUI
    - Web / HTTP
    - Dashboard
    - Kiosk
- Modular Checksum Support
    - Damm Algorithm
    - Verhoeff Algorithm
    - Luhn Algorithm (Legacy support)
