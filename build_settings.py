COMMON_PATH = 'common/'
BUILD_PATH = 'build/'
SAME_VERSION = 'MC_0'

EXTRA_FILE = ['README.md', 'LICENSE'] 
# relative to project root

EXCLUDE_FILE = ['spyglass.json'] 
# relative to version source root

MC_1_16_X = {'path': '1_16_x/', 'name': 'FloatingIslands-Datapack_v{version}_1.16.x', 'version': '1.2.0'}
MC_1_17_X = {'path': '1_17_x/', 'name': 'FloatingIslands-Datapack_v{version}_1.17.x', 'version': '1.1.0'}
MC_1_18_1 = {'path': '1_18_1/', 'name': 'FloatingIslands-Datapack_v{version}_1.18.1', 'version': '2.0.2'}
MC_1_18_2 = {'path': '1_18_2/', 'name': 'FloatingIslands-Datapack_v{version}_1.18.2', 'version': '2.1.1'}
MC_1_19_3 = {'path': '1_19_3/', 'name': 'FloatingIslands-Datapack_v{version}_1.19.3', 'version': '3.0.2'}
MC_1_19_4 = {'path': '1_19_4/', 'name': 'FloatingIslands-Datapack_v{version}_1.19.4', 'version': '3.1.2'}
MC_1_20_1 = {'path': '1_20_1/', 'name': 'FloatingIslands-Datapack_v{version}_1.20.1', 'version': '3.2.1'}
MC_1_20_4 = {'path': '1_20_4/', 'name': 'FloatingIslands-Datapack_v{version}_1.20.4', 'version': '3.3.1'}
MC_1_20_6 = {'path': '1_20_6/', 'name': 'FloatingIslands-Datapack_v{version}_1.20.6', 'version': '3.4.1'}
MC_1_21 = {'path': '1_21/', 'name': 'FloatingIslands-Datapack_v{version}_1.21', 'version': '3.5.0'}


def __collect_constant() -> dict:
    ret = {}
    global_temp = globals().copy()
    for key in global_temp:
        if key.startswith('MC_'):
            ret[key] = global_temp[key]
    # ret.pop(*['COMMON_PATH', 'BUILD_PATH', 'SAME_VERSION', 'EXTRA_FILE', 'EXCLUDE_FILE'])
    return ret

__VERSION_CONFIG = __collect_constant()
