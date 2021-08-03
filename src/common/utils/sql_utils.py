import base64
import json


def get_str(x):
    return str(x).replace('"', "'")


def dict_to_b64_str(to_convert: dict) -> str:
    b = bytes(json.dumps(dict(sorted(to_convert.items()))), 'utf-8')
    return base64.b64encode(b).decode('utf-8')


def b64_str_to_dict(to_convert: str) -> dict:
    return json.loads(base64.b64decode(to_convert))


def get_field_val_for_query(value):
    if value is None:
        return 'null'
    if isinstance(value, int) or isinstance(value, float):
        return value
    if isinstance(value, list):
        return f'({",".join(list(map(lambda x: get_field_val_for_query(x), value)))})'
    if isinstance(value, str):
        return f'"{value}"'
