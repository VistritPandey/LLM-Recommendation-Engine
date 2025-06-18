from importlib import import_module
from .base import BaseStorage  # noqa: F401


def storage_from_path(path: str, **kwargs):
    module_path, cls_name = path.rsplit(".", 1)
    mod = import_module(module_path)
    cls = getattr(mod, cls_name)
    return cls(**kwargs) 