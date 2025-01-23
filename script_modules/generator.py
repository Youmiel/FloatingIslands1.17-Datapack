import importlib
import os
import sys
import typing as ty
from pathlib import Path
from types import ModuleType

from script_modules import file_util, io_util
from script_modules.resource_locator import VersionResourceManager


def get_source_full_path(key: str, relative_source: Path, res_manager: VersionResourceManager):
    if key is None:
        return None
    elif key == 'COMMON':
        return res_manager.get_common_source_path(relative_source)
    else:
        return res_manager.get_built_file_path(key, relative_source)


def clean_directory(build_dir: ty.Union[str, Path]) -> bool:
    if not os.path.exists(build_dir):
        os.makedirs(build_dir)
    if not file_util.clean_dir(build_dir):
        print('  Clean build directory fail.', file=sys.stderr)
        return False
    return True


def scan_sources(res_manager: VersionResourceManager):
    source_file_list: ty.List[str] = file_util.scan_folder(res_manager.get_current_version_root())
    patch_file_list, static_file_list = [], []
    patch_predicate, chache_predicate = file_util.extension_match('.py'), file_util.part_match('__pycache__')
    for filename in source_file_list:
        if patch_predicate(filename):
            patch_file_list.append(filename)
        elif not chache_predicate(filename):
            static_file_list.append(filename)
        else:
            pass
    return (static_file_list, patch_file_list)


def collect_json(version_key: str, source: Path, patch_module: ModuleType, res_manager: VersionResourceManager):
    if version_key is None:
        return
    source_full_path = get_source_full_path(version_key, source, res_manager)
    charset = io_util.get_charset(source_full_path)
    return io_util.read_json_dict(source_full_path, charset)


def patch_json(rel_patch_path: Path, patch_module: ModuleType, res_manager: VersionResourceManager): 
    file_ref = patch_module.reference_file(rel_patch_path, res_manager.get_current_version_config())
    if isinstance(file_ref, tuple): # single file
        version_key, relative_source, target_path_o = file_ref
        t_source_content = (target_path_o, collect_json(version_key, relative_source, patch_module, res_manager))

        t_modified_content: ty.Tuple[Path, ty.Dict[str, ty.Any]] = patch_module.process_single(t_source_content)

        target_path_m, dict_content = t_modified_content
        full_target_path = res_manager.get_current_build_version_root().joinpath(target_path_m)
        os.makedirs(full_target_path.parent, exist_ok=True)
        io_util.write_json_dict(t_modified_content[1], full_target_path)
    elif isinstance(file_ref, list): # multi-file
        lt_source_content = []
        for version_key, relative_source, target_path_o in file_ref:
            lt_source_content.append(
                (target_path_o, collect_json(version_key, relative_source, patch_module, res_manager)))

        lt_modified_content: ty.Tuple[Path, ty.Dict[str, ty.Any]] = patch_module.process_multi(lt_source_content)

        for target_path_m, dict_content in lt_modified_content:
            full_target_path = res_manager.get_current_build_version_root().joinpath(target_path_m)
            os.makedirs(full_target_path.parent, exist_ok=True)
            io_util.write_json_dict(dict_content, full_target_path)
    else: # None or other, ingore
        pass


def process_patch(source_version_root: Path, patch_strpath: str, res_manager: VersionResourceManager):
    relative_patch_path = Path(patch_strpath).relative_to(source_version_root)
    module_name = '.'.join(Path(patch_strpath).with_suffix('').parts)
    patch_module = importlib.import_module(module_name)

    # only handles json now
    if patch_module.TYPE == 'json':
        patch_json(relative_patch_path, patch_module, res_manager)
    else:
        print(f'    Unhandled patch {relative_patch_path}')