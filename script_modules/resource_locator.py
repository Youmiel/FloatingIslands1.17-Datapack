import os
from pathlib import Path
import sys
from typing import Dict


class VersionResourceManager():
    def __init__(
            self, 
            build_path: Path, 
            common_path: Path, 
            same_version_keyword: str, 
            version_config: Dict[str, str]
        ):
        self.build_path = build_path
        self.common_path = common_path
        self.same_version_keyword = same_version_keyword
        self.version_config = version_config

        self._current_verion = None
    
    def set_currrent_version(self, version_key: str):
        if version_key not in self.version_config:
            print(f'The version {version_key} is not in config.', file=sys.stderr)
            return
        self._current_verion = version_key

    def get_current_version(self) -> str:
        if self._current_verion is None:
            print(f'Current version is not set.', file=sys.stderr)
        return self._current_verion

# ?
    def get_current_version_config(self) -> Dict[str, str]:
        return self.version_config[self._current_verion]

# # ?
#     def get_current_version_config_path(self) -> str:
#         return self.get_current_version_config()['path']


    def get_version_root(self, version_key: str) -> Path:
        if version_key == self.same_version_keyword and self._current_verion is not None:
            return self.version_config[self._current_verion]['path']
        return self.version_config[version_key]['path']

    def get_built_version_root(self, version_key: str) -> Path:
        return self.build_path / self.get_version_root(version_key)

    def get_current_version_root(self) -> Path:
        return self.get_version_root(self._current_verion)

    def get_current_build_version_root(self) -> Path:
        return self.get_built_version_root(self._current_verion)


    def get_common_source_path(self, resource: Path) -> Path:
        return self.common_path / resource

    def get_source_path(self, version_key: str, resource: Path) -> Path:
        return self.get_version_root(version_key) / resource

    def get_built_file_path(self, version_key: str, resource: Path) -> Path:
        return self.get_built_version_root(version_key) / resource


