# coding: utf-8

import importlib.resources
from ksupk import singleton_decorator


@singleton_decorator
class ResourceManager:
    def __init__(self):
        self.package_name = "GDV_feature_shows"
        self.package_assets_folder = "assets"

    def file_path(self, file_path) -> str or None:
        res = None
        with importlib.resources.path(f"{self.package_name}.{self.package_assets_folder}", file_path) as tmp_file_path:
            res = str(tmp_file_path)
        return res

    def ico_path(self) -> str:
        return self.file_path("ico.png")
