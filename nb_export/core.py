# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/00_core.ipynb (unless otherwise specified).

__all__ = ['read_nb', 'nb_iter', 'code_iter', 'extract_code', 'build_all']

# Cell
import json
import re
from collections import defaultdict

# Cell
def read_nb(nb_path):
    return  json.load(nb_path.open())

# Cell
def nb_iter(base_path):
    return base_path.glob('*.ipynb')

# Cell
def code_iter(nb):
    for cell in nb['cells']:
        if cell['cell_type']=='code':
            if cell['source']:
                yield cell['source']

# Cell
def extract_code(nb, pre=None):
    to_export = defaultdict(list)

    for code in code_iter(nb):
        # Can't get python 3.8 to work with github CI
        # if match := re.match(r'''# exp (.+)\n''', code[0]):
        match = re.match(r'''# exp (.+)\n''', code[0])
        if match:
            target = match.group(1)
            content = ''.join(code[1:])
            if pre is not None:
                content = '#' + pre + '\n' + content

            to_export[target].append(content)
    return to_export

# Cell
def build_all(read_base_path, save_base_path=None):
    dicts = [extract_code(read_nb(nb_path), pre=nb_path.name) for nb_path in nb_iter(Path(read_base_path))]
    if save_base_path is None: save_base_path=Path(read_base_path)

    merged = dicts[0]
    for single_dict in dicts[1:]:
        for key,value in single_dict.items():
            merged[key] += value

    # sort imports to top
    imports = []
    regular = []

    for file in merged.keys():
        for cell in merged['common']:
            if 'import ' in cell:
                imports.append(cell)
            else:
                regular.append(cell)

        full_text = '\n'.join(imports) + '\n\n#-----\n\n' + '\n\n'.join(regular)
        filename = save_base_path / f'{file}.py'

        with open(filename, 'w') as f:
            f.write(full_text)