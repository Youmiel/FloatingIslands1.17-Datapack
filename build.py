# all the file extension are separated with triple '_'
# e.g. 
# pack___mcmeta.py: meta file patch
# xxx___json.py: single file patch
# yyy___multi.py: multiple file patch
# zzz.json: static resource

from pathlib import Path
import os
import typing as ty

import build_settings as settings

from script_modules.resource_locator import VersionResourceManager
from script_modules import file_util
from script_modules import generator


def run(
        build_path: str, 
        common_path: str, 
        same_version_keyword: str, 
        version_config: ty.Dict[str, ty.Any],
        extra_file_list: ty.List[str],
        exclude_file_list: ty.List[str]
    ):
    res_manager = VersionResourceManager(Path(build_path), Path(common_path), same_version_keyword, version_config)

    for v_key in version_config:
        res_manager.set_currrent_version(v_key) 

        build_version_root = res_manager.get_current_build_version_root()
        source_version_root = res_manager.get_current_version_root()
        print(f'Start building version {v_key} ...')

        print(f'  Cleaning build directory {build_version_root} ...')
        if not generator.clean_directory(build_version_root):
            continue

        print(f'  Scanning {source_version_root} ...')
        static_file_list, patch_file_list = generator.scan_sources(res_manager, exclude_file_list)

        print('  Copying static file...')
        static_destination_list = [os.path.join(build_version_root, os.path.relpath(file, source_version_root)) for file in static_file_list]
        # need verification
        file_util.copy_file(static_file_list, static_destination_list)

        print('  Processing patches...')
        src_version_root = res_manager.get_current_version_root()
        for patch_strpath in patch_file_list:
            generator.process_patch(src_version_root, patch_strpath, res_manager)
            
        print('  Packing...')
        generator.pack_zipfile(Path(build_path), build_version_root, res_manager.get_current_version_config(), extra_file_list)


if __name__ == '__main__':
    run(settings.BUILD_PATH, settings.COMMON_PATH, 
        settings.SAME_VERSION, settings.__VERSION_CONFIG, 
        settings.EXTRA_FILE, settings.EXCLUDE_FILE)