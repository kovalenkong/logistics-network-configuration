import json

import yaml

from .exceptions import UnsupportedFileExtension


def export_data(filename: str, data: dict | list):
    export_functions = {
        'yaml': yaml.dump,
        'yml': yaml.dump,
        'json': json.dump,
    }
    extension = filename.split('.')[-1]
    if extension not in export_functions:
        raise UnsupportedFileExtension(
            f'Unsupported file extension: "{extension}"'
        )
    with open(filename, 'w') as f:
        export_functions[extension](data, f)


def import_data(filename: str) -> dict | list:
    extension = filename.split('.')[-1].lower()
    import_functions = {
        'yaml': (yaml.load, {'Loader': yaml.CLoader}),
        'yml': (yaml.load, {'Loader': yaml.CLoader}),
        'json': (json.loads, {}),
    }
    if extension not in import_functions:
        raise UnsupportedFileExtension(
            f'Unsupported file extension: "{extension}"'
        )
    with open(filename) as f:
        func, f_kwargs = import_functions[extension]
        return func(f.read(), **f_kwargs)
