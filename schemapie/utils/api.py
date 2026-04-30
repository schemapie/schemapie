from schemapie.utils.os import display, read, write
import requests

TYPE_MAP = {
    'dict': 'Object',
    'list': 'Array',
    'str': 'String',
    'int': 'Integer',
    'float': 'Number',
    'bool': 'Boolean',
    'NoneType': 'Null',
}

def get_type(object: any):
    return TYPE_MAP.get(type(object).__name__)

def flatten(data: dict | list, path: str = "", meta: dict = None, verbose: bool = False):
    """Flattens each object in the API response into a dictionary object containing {path: details}."""
    if meta is None:
        meta = {}

    if isinstance(data, dict):
        for k, v in data.items():
            meta.setdefault(f"{path}{k}", {"path": f"{path}{k}" if path else k, "type": get_type(v)})
            if isinstance(v, (dict, list)):
                flatten(data=v, path=f"{path}{k}.", meta=meta, verbose=verbose)
            else:
                meta[f"{path}{k}"].setdefault("examples", set()).add(v) if verbose else meta[f"{path}{k}"].setdefault("examples", {v})

    elif isinstance(data, list):
        for v in data:
            if isinstance(v, (dict, list)):
                meta[f"{path[:-1]}"].update({"type": f"{get_type(data)}[{get_type(v)}]"})
            else: 
                meta[f"{path[:-1]}"].update({"type": f"{get_type(data)}[{get_type(v)}]"})
                meta[f"{path[:-1]}"].setdefault("examples", set()).add(v) if verbose else meta[f"{path[:-1]}"].setdefault("examples", {v})
            flatten(data=v, path=path, meta=meta, verbose=verbose)

    return meta

def merge(meta: dict, schema: dict = {}):
    """Loops through the flattened API response data that was created by the flatten function."""
    for key, value in meta.items():
        path = key.split('.')
        build(schema=schema, path=path, value=value)

    return schema

def build(schema: dict, path: list, value: dict):
    """Constructs the schema one object at a time."""
    current = schema
    for i, p in enumerate(path):
        if p not in current:
            current[p] = {}

        if i == len(path) - 1:
            if value.get("examples"):
                value["examples"] = list(value["examples"])
            current[p].update(value)
        else:
            current[p].setdefault("children", {})
            current = current[p]["children"]

def execute(url: str, file: str = None, verbose: bool = False):
    print(f"Fetching data from {url}...")

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        meta = flatten(data=data, verbose=verbose)
        schema = merge(meta=meta, schema=read(file=file) if file else {})
        write(schema=schema, file=file) if file else display(schema=schema)
    else:
        print(f"Error: {response.status_code} - {response.text}")