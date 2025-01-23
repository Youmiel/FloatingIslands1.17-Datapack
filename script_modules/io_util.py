import json
import os
from pathlib import Path
import typing as ty
import chardet

def get_charset(file_path: ty.Union[str, Path]) -> str:
    with open(file_path, 'br') as byte_content:
        return chardet.detect(byte_content.read())['encoding']


def read_json_dict(file_path: ty.Union[str, Path], charset: str) -> ty.Dict[str, ty.Any]:
    with open(file_path, 'r', encoding=charset) as json_file:
        return json.load(json_file)


def write_json_dict(content: ty.Dict[ty.Any, ty.Any], file_path: ty.Union[str, Path], charset: str = 'utf8'):
    with open(file_path, 'w', encoding=charset) as json_file:
        json.dump(content, json_file, indent=2, default=lambda obj: obj.__dict__)
