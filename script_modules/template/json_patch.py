from pathlib import Path
import typing as ty

TYPE = 'json'

def reference_file(patch_path: Path, patch_version_config: ty.Dict[str, str]) \
     -> ty.Union[ty.Tuple[str, Path], ty.List[ty.Tuple[str, Path]], None]:
    '''
    Provides the target resource file(s) to patch generator.
    Due to the generation order, this only allows reference to 
    older MC versions or non-patch resources in current version.

    args: 
    - patch_path: (read-only) the relative path of the patch (without version directory)
    - patch_version_config: (read-only) current version config

    returns:
    - (version_id, relative_path, new_path): version_id is the constant names in build_settings.py. \
        relative_path is the relative path to the target resource in build dir. new_path is the path \
        to generated result.
    - list of (version_id, relative_path, new_path): the same as above.
    - None: references nothing, the patch will be ignored.
    '''

    '''
    file_name = patch_path.with_suffix('').with_name(patch_path.stem.replace('___','.'))

    # reference to single file, MC_1_16_X is a constant defined in 'build_settings.py'
    return ('MC_1_16_X', file_name, file_name)

    # reference to a non-patch file in current version
    return ('MC_0', Path(patch_version_config['path']) / 'some/path.json', file_name)

    # reference to arbitary file
    return (None, Path('some/random/path.json'), file_name)

    # reference to multi file
    if patch_path.stem.endswith('___multi'):
        return [
            ('MC_1_16_X', patch_path.parent / 'example1.json', patch_path.parent / 'example1.json'),
            ('MC_1_16_X', patch_path.parent / 'example2.json', patch_path.parent / 'example2.json'),
            ('COMMON', patch_path.parent / 'example3.json', patch_path.parent / 'example3.json'),
        ]
    '''

    # reference to nothing
    return None

def process_single(content: ty.Tuple[Path, ty.Dict]) -> ty.Tuple[Path, ty.Dict]:
    '''
    Precesses the content from a single file.

    args:
    - content: (new_path, dict_content): new_path is the path to the generated file, \
        dict_content is the content deserialized from the source json.

    returns:
    - (new_path, dict_content): modified content
    '''
    return {}

def process_multi(content: ty.List[ty.Tuple[Path, ty.Dict]]) -> ty.List[ty.Tuple[Path, ty.Dict]]:
    '''
    Processes the content from a single file.

    args:
    - content: list of (new_path, dict_content): new_path is the path to the generated file, \
        dict_content is the content deserialized from the source json.

    returns:
    - list of (new_path, dict_content): modified contents
    '''
    return []