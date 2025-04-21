import os
from pathlib import Path
from polib import pofile

BASE_DIR = Path(__file__).resolve().parent
locale_path = BASE_DIR / 'locale'

for lang_dir in locale_path.iterdir():
    lc_messages = lang_dir / 'LC_MESSAGES'
    if lc_messages.exists():
        for po_file in lc_messages.glob('*.po'):
            mo_file = lc_messages / (po_file.stem + '.mo')
            pofile(str(po_file)).save_as_mofile(str(mo_file))
            print(f'✔ Compiled: {mo_file}')
