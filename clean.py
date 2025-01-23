import os
import shutil
import sys
from script_modules import file_util

sys.dont_write_bytecode = True

EXCLUDE_SUB_FOLDER = ['include', 'lib', 'scripts', '.git'
                      'build']

if __name__ == '__main__':
    cache_path_predicate = file_util.part_match(path_part='__pycache__')
    cache_ext_predicate = file_util.extension_match('.pyc')

    print('Scanning cache...')
    all_sub_folder_list = os.listdir('.')
    potential_cache_list = []
    for sub_dir in all_sub_folder_list:
        if os.path.isfile(sub_dir):
            continue
        if sub_dir.lower() in EXCLUDE_SUB_FOLDER:
            continue
        potential_cache_list.extend(file_util.scan_folder(sub_dir))
    cache_folder_set = set(os.path.dirname(item) for item in potential_cache_list if cache_path_predicate(item))

    print('Cleaning cache...')
    for cache_folder in cache_folder_set:
        print(cache_folder)
        shutil.rmtree(cache_folder)