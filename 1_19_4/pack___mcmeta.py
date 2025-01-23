from pathlib import Path
import typing as ty

TYPE = 'json'

PACK_FORMAT = 12

version_cache = '0.0.0'

def reference_file(patch_path: Path, patch_version_config: ty.Dict[str, str]) \
        -> ty.Union[ty.Tuple[str, Path], ty.List[ty.Tuple[str, Path]], None]:
    file_name = patch_path.with_suffix('').with_name(patch_path.stem.replace('___','.'))
    version_cache = patch_version_config['version']

    return ('COMMON', Path('pack.mcmeta'), file_name)

def process_single(content: ty.Tuple[Path, ty.Dict]) -> ty.Tuple[Path, ty.Dict]:
    new_path, json_content = content
    json_content['pack']['pack_format'] = PACK_FORMAT
    json_content['pack']['version'] = version_cache
    return (new_path, json_content)

def process_multi(content: ty.List[ty.Tuple[Path, ty.Dict]]) -> ty.List[ty.Tuple[Path, ty.Dict]]:
    return []