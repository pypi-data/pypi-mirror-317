import os
import json
import yaml

DEFAULT_ENCODING = 'utf-8'

def find_file(path, file_name):
    for root, dirs, files in os.walk(path):
        if file_name in files:
            return os.path.join(root, file_name)


def find_dirs(path):
    results = []
    for root, dirs, files in os.walk(path):
        for d in dirs:
            results.append(d)
    return results


def list_file(path):
    files = []
    for file_name in sorted(os.listdir(path)):
        files.append(os.path.join(path, file_name))
    return files


def save_dict(path, target_dict, encoding=DEFAULT_ENCODING):
    with open(path, 'w', encoding=encoding) as f:
        json.dump(target_dict, f)


def load_dict(path, encoding=DEFAULT_ENCODING):
    with open(path, encoding=encoding) as f:
        return json.load(f)


# Deprecated
def write_yaml(file_path, obj, encoding=DEFAULT_ENCODING):
    with open(file_path, 'w', encoding=encoding) as f:
        yaml.dump(obj, f, allow_unicode=True, default_flow_style=False, sort_keys=False)


def save_yaml(file_path, obj, encoding=DEFAULT_ENCODING):
    with open(file_path, 'w', encoding=encoding) as f:
        yaml.dump(obj, f, allow_unicode=True, default_flow_style=False, sort_keys=False)


def load_yaml(file_path, encoding=DEFAULT_ENCODING):
    with open(file_path, 'r', encoding=encoding) as f:
        data = yaml.safe_load(f)
    return data
