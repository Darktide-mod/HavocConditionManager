"""Stage plain built-in packages; never embed or extract their contents."""
from pathlib import Path
import json
import shutil

PROJECT = Path(__file__).resolve().parents[1]
SOURCE = PROJECT / 'custom-packages/template-library'
# Other editable examples are development material, not built-in conditions.
BUILTIN = ('starter-conditions-no_healing',)
OUTPUT = PROJECT / 'src/HavocConditionManager/diy'


def build():
    count = 0
    for package_id in BUILTIN:
        folder = SOURCE / package_id
        manifest = json.loads((folder / 'package.json').read_text(encoding='utf-8-sig'))
        assert manifest['id'] == folder.name
        names = ['package.json'] + manifest['files']
        for name in names:
            target=OUTPUT/'packages'/package_id/name
            target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(folder/name,target)
        count += 1
    (OUTPUT/'index.json').write_text(json.dumps({'version':1,'packages':list(BUILTIN)},indent=2)+'\n',encoding='utf8')
    print(f'Staged {count} built-in packages as plain files')


if __name__ == '__main__':
    build()
