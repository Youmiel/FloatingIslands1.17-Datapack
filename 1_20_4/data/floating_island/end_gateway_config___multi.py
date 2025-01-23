from pathlib import Path
import typing as ty

TYPE = 'json'

def reference_file(patch_path: Path, patch_version_config: ty.Dict[str, str]) \
     -> ty.Union[ty.Tuple[str, Path], ty.List[ty.Tuple[str, Path]], None]:

    # common_path = Path('data/floating_island/worldgen')
    common_path = patch_path.parent / 'worldgen'

    path_portal_feature = common_path / 'configured_feature' / 'end_gateway_return_0_0.json'
    path_placed_nether = common_path / 'placed_feature' / 'end_gateway_return_nether.json'
    path_placed_overworld = common_path / 'placed_feature' / 'end_gateway_return_overworld.json'
    path_placed_warped = common_path / 'placed_feature' / 'end_gateway_return_warped.json'
    
    return [
        ('MC_1_19_3', path_portal_feature, path_portal_feature),
        ('MC_1_19_3', path_placed_nether, path_placed_nether),
        ('MC_1_19_3', path_placed_overworld, path_placed_overworld),
        ('MC_1_19_3', path_placed_warped, path_placed_warped)
    ]


def process_multi(content: ty.List[ty.Tuple[Path, ty.Dict]]) -> ty.List[ty.Tuple[Path, ty.Dict]]:
    return content