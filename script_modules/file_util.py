import os
import re
import shutil
import sys
import typing as ty
from pathlib import Path


def always_true(*args, **kwargs) -> bool:
    return True


def extension_match(ext: str) -> ty.Callable[[str], bool]:
    # the 'path' argument is the full path in usual conditions
    def match_function(path: str) -> bool:
        return os.path.splitext(path)[1] == ext
    return match_function


def extension_match_regex(ext_pattern: re.Pattern) -> ty.Callable[[str], bool]:
    def match_function(path: str) -> bool:
        return re.match(ext_pattern, os.path.splitext(path)[1]) is not None
    return match_function


def basename_match_regex(name_pattern: re.Pattern) -> ty.Callable[[str], bool]:
    def match_function(path: str) -> bool:
        return re.match(name_pattern, path) is not None
    return match_function


def part_match(path_part: str) -> ty.Callable[[str], bool]:
    def match_function(path: str) -> bool:
        return path.find(path_part) > 0
    return match_function

       
def scan_folder(start_path: str, max_recursion: int = 15, log: bool = False, file_predicate: ty.Callable[[str], bool] = always_true) -> ty.List[str]:
    '''
    args:
    - start_path: 
    - max_recursion: 
    - log:
    - file_predicate: receives file basename, returns whether it is accepted, e.g. file_predicate('sample.txt').
    '''
    result = []
    sub_path = os.listdir(start_path)
    if log:
        print('Scanning', start_path, '...', len(sub_path), 'files/directories')
    for sub in sub_path:
        full_path = os.path.join(start_path, sub)
        if os.path.isfile(full_path) and file_predicate(sub):
            result.append(full_path)
        elif max_recursion != 0 and os.path.isdir(full_path):
            result.extend(scan_folder(full_path, max_recursion - 1, log, file_predicate))
    return result


def clean_dir(directory: ty.Union[str, Path]) -> bool:
    if not os.path.exists(directory):
        print(f'The path {directory} is not exist!')
        return False

    if os.path.isfile(directory):
        print(f'The path {directory} is not a directory!')
        return False
    
    sub_path = os.listdir(directory)
    for sub in sub_path:
        full_path = os.path.join(directory, sub)
        if os.path.isfile(full_path):
            os.remove(full_path)
        else:
            shutil.rmtree(full_path)
    return True


def recreate_dir(directory: ty.Union[str, Path]) -> bool:
    if not os.path.exists(directory):
        print(f'The path {directory} is not exist!')
        return False

    if os.path.isfile(directory):
        print(f'The path {directory} is not a directory!')
        return False

    shutil.rmtree(directory)
    os.makedirs(directory, exist_ok=True)
    return True


def create_dirs(path_list: str | ty.List[str]) -> bool:
    '''retruns true if the creations are all succeeded'''
    if isinstance(path_list, str):
        path_list = [path_list]
    path_list.sort(key=lambda p: len(p), reverse=True)
    no_exception = True
    for p in path_list:
        try:
            if not os.path.exists(p):
                os.makedirs(p, exist_ok=True)
        except OSError as e:
            print(e, file=sys.stderr)
            no_exception = False
    return no_exception
    

def copy_file(source_list: str | ty.List[str], destination_list: str | ty.List[str]) -> bool:
    ''' should not include directories'''
    if len(source_list) != len(destination_list):
        print('The length of source and destination list do not match', file=sys.stderr)
        return False

    dir_list = [os.path.dirname(p) for p in destination_list]
    if not create_dirs(dir_list):
        return False

    file_count = len(source_list)
    no_exception = True
    for i in range(file_count):
        try:
            shutil.copy(source_list[i], destination_list[i])
        except shutil.SameFileError as sfe:
            print(sfe, file=sys.stderr)
            no_exception = False
    return no_exception

