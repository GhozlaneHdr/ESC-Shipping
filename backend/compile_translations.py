"""
Compile .po files to .mo files using polib.
Run: python compile_translations.py
"""

import polib
from pathlib import Path

locale_dir = Path(__file__).parent / "locale"

for po_file in locale_dir.rglob("*.po"):
    mo_file = po_file.with_suffix(".mo")
    po = polib.pofile(str(po_file))
    po.save_as_mofile(str(mo_file))
    print(f"Compiled: {po_file.relative_to(locale_dir)} -> {mo_file.relative_to(locale_dir)}")

print("\nAll translations compiled successfully.")
